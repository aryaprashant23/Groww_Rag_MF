import os
import datetime
from typing import Dict, Any
from dotenv import load_dotenv

# Set up Langchain imports
import langchain

from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from tenacity import retry, wait_exponential, stop_after_attempt

# Load environment variables (GROQ_API_KEY)
load_dotenv()

# Caching has been temporarily disabled due to version mismatch

# Strict system prompt for the Groq LLM
SYSTEM_PROMPT = """You are a strictly factual mutual fund assistant.
Use ONLY the provided context chunks to answer the user's question.
If the answer is not contained in the context, say "I don't have enough information to answer that."
Keep your answer to a strict maximum of 3 sentences.
Do NOT provide investment advice.

You must extract the exact Source URL from the chunk metadata that you used to answer the question, and include it at the very end of your response on a new line in this exact format:
URL: <the_url>

You must also extract the date of the data (e.g., the NAV date) from the context and include it on a new line in this exact format:
DATE: <the_date>

Context:
{context}
"""

class RAGPipeline:
    def __init__(self):
        # 1. Semantic Retriever Setup (BGE Small)
        print("Initializing BGE Embeddings for RAG Pipeline...")
        model_name = "BAAI/bge-small-en-v1.5"
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': True}
        
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        
        vectorstore_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma_db")
        self.vectorstore = Chroma(
            persist_directory=vectorstore_dir,
            embedding_function=self.embeddings
        )
        
        # Fetch top-10 chunks to ensure maximum context and accuracy
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={'k': 10}
        )

        # 2. LLM Setup (Groq llama-3.3-70b-versatile)
        print("Initializing Groq LLM...")
        # ChatGroq natively supports max_retries for API limits (429s) with backoff
        self.llm = ChatGroq(
            temperature=0, # Deterministic, factual
            model_name="llama-3.3-70b-versatile",
            max_retries=3
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "{question}")
        ])
        
    def _format_docs(self, docs):
        """Format retrieved documents into a single string with their source URLs."""
        context = ""
        for i, d in enumerate(docs):
            url = d.metadata.get("source_url", "Unknown")
            context += f"[Document {i+1}]\nSource URL: {url}\nContent: {d.page_content}\n\n"
        return context

    # Adding an explicit tenacity wrapper for added safety against arbitrary network errors
    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
    def _invoke_llm(self, context: str, question: str) -> str:
        chain = self.prompt | self.llm
        response = chain.invoke({"context": context, "question": question})
        return response.content

    def get_answer(self, query: str) -> Dict[str, Any]:
        """
        Main RAG function to retrieve context, generate answer, and format output.
        """
        try:
            # Step 1: Semantic Retrieval
            docs = self.retriever.invoke(query)
            
            if not docs:
                return {
                    "answer": "I couldn't find relevant factual information for your query in my database.",
                    "sources": [],
                    "raw_answer": ""
                }
                
            context = self._format_docs(docs)
            
            # Step 2: Generation via Groq
            raw_answer = self._invoke_llm(context, query)
            
            # Extract URL and DATE from raw_answer
            used_urls = []
            answer_text = []
            extracted_date = None
            
            for line in raw_answer.split('\n'):
                if line.strip().startswith("URL:"):
                    used_urls.append(line.replace("URL:", "").strip())
                elif line.strip().startswith("DATE:"):
                    extracted_date = line.replace("DATE:", "").strip()
                else:
                    answer_text.append(line)
            
            clean_answer = "\n".join(answer_text).strip()
            
            # Step 3: Output Formatting
            if extracted_date:
                date_str = extracted_date
            else:
                date_str = datetime.datetime.now().strftime("%Y-%m-%d")
                
            footer = f"\n\nLast updated from sources: {date_str}"
            
            if used_urls:
                # Deduplicate and format
                unique_urls = list(set(used_urls))
                sources_text = "\nSource(s):\n" + "\n".join([f"- [{url}]({url})" for url in unique_urls])
            else:
                unique_urls = []
                sources_text = ""
                
            final_answer = f"{clean_answer}\n{sources_text}{footer}"
            
            return {
                "answer": final_answer,
                "sources": unique_urls,
                "raw_answer": raw_answer
            }
            
        except Exception as e:
            # Graceful error handling for Rate Limits and other exceptions
            error_msg = str(e).lower()
            if "429" in error_msg or "rate_limit" in error_msg or "too many requests" in error_msg:
                return {
                    "answer": "I am currently receiving too many requests due to API limits. Please try again in a few moments.",
                    "sources": [],
                    "raw_answer": ""
                }
            return {
                "answer": "An unexpected error occurred while generating the response. Please try again.",
                "sources": [],
                "raw_answer": ""
            }

if __name__ == "__main__":
    # Test the pipeline interactively
    pipeline = RAGPipeline()
    print("\n--- RAG Pipeline Interactive Test ---")
    print("Type 'quit' or 'exit' to stop.")
    
    while True:
        try:
            user_query = input("\nEnter your query: ").strip()
            if user_query.lower() in ['quit', 'exit']:
                break
            if not user_query:
                continue
                
            print("-" * 50)
            result = pipeline.get_answer(user_query)
            print(result["answer"])
            print("-" * 50)
        except (KeyboardInterrupt, EOFError):
            break

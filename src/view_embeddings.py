import os
import sys
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma

def main():
    print("Loading Vector Storage (ChromaDB)...")
    vectorstore_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma_db")
    
    if not os.path.exists(vectorstore_dir):
        print(f"Error: Database not found at {vectorstore_dir}.")
        print("Please run 'python src/ingest.py' in your virtual environment to generate the database first.")
        sys.exit(1)

    # Initialize the same embedding model used during ingestion
    print("Initializing BGE Small embedding model...")
    model_name = "BAAI/bge-small-en-v1.5"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    
    # Connect to the existing Chroma database
    vectorstore = Chroma(
        persist_directory=vectorstore_dir,
        embedding_function=embeddings
    )
    
    # Fetch some data from the database using the underlying Chroma collection
    collection = vectorstore._collection
    count = collection.count()
    print(f"\nTotal chunks stored in the database: {count}")
    
    if count == 0:
        print("The database is empty.")
        return

    print("\nFetching the first 3 chunks and their embeddings for review...")
    # Get the first 3 items including their embeddings, documents, and metadatas
    results = collection.get(limit=3, include=["embeddings", "documents", "metadatas"])
    
    for i in range(len(results["ids"])):
        print("-" * 60)
        print(f"Chunk ID: {results['ids'][i]}")
        print(f"Source URL: {results['metadatas'][i].get('source_url', 'Unknown')}")
        print(f"Text Snippet: {results['documents'][i][:150]}...")
        
        embedding = results["embeddings"][i]
        print(f"\nEmbedding Dimension: {len(embedding)}")
        print(f"Embedding Array (first 5 values): {embedding[:5]}")
        print("-" * 60)

if __name__ == "__main__":
    main()

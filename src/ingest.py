import os
import sys

# Ensure the script can import scraper
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scraper import scrape_all

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma

def main():
    print("--- Phase 1: Environment Setup & Data Ingestion ---")
    
    # Step 2: Web Scraping
    print("\n[Step 2] Web Scraping...")
    docs_data = scrape_all()
    
    # Save scraped data to files so it can be reviewed
    print("Saving scraped data to 'data' directory for review...")
    os.makedirs("data", exist_ok=True)
    for doc in docs_data:
        filename = doc["url"].split("/")[-1]
        filepath = os.path.join("data", f"{filename}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"URL: {doc['url']}\n\n")
            f.write(doc["text"])
    
    # Step 3: Chunking & Metadata Tagging
    print("\n[Step 3] Chunking & Metadata Tagging...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )
    
    chunks = []
    metadatas = []
    
    for doc in docs_data:
        splits = text_splitter.split_text(doc["text"])
        chunks.extend(splits)
        # Inject the source URL into each chunk's metadata
        metadatas.extend([{"source_url": doc["url"]} for _ in splits])
        
    print(f"Total chunks created: {len(chunks)}")
    
    if not chunks:
        print("Error: No chunks were created. This usually means the web scraper was blocked (e.g., by Cloudflare Bot Protection). Aborting ingestion to preserve the old database.")
        sys.exit(1)
    
    # Step 4: Vector Storage Setup
    print("\n[Step 4] Initializing BGE embedding model...")
    model_name = "BAAI/bge-small-en-v1.5"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    
    print("Setting up Vector Storage (ChromaDB) in a temporary directory...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vectorstore_dir = os.path.join(base_dir, "chroma_db")
    temp_vectorstore_dir = os.path.join(base_dir, "chroma_db_temp")
    
    import shutil
    if os.path.exists(temp_vectorstore_dir):
        shutil.rmtree(temp_vectorstore_dir)
        
    print(f"Creating new vector database at {temp_vectorstore_dir}...")
    
    # Store chunks in temporary Chroma DB
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=temp_vectorstore_dir
    )
    
    # Force persist if using an older chromadb version (ignored in newer versions)
    if hasattr(vectorstore, "persist"):
        vectorstore.persist()
        
    print(f"Successfully created new database. Replacing old database...")
    
    # Replace old db with new db
    if os.path.exists(vectorstore_dir):
        try:
            shutil.rmtree(vectorstore_dir)
        except Exception as e:
            print(f"Warning: Could not remove old database (it might be locked by the API server). Error: {e}")
            print(f"The new database is available at {temp_vectorstore_dir}")
            return
            
    os.rename(temp_vectorstore_dir, vectorstore_dir)
    
    print(f"\nData ingestion complete! Vector DB successfully saved to '{vectorstore_dir}'.")

if __name__ == "__main__":
    main()

import os
import sys
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma

def main():
    vectorstore_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma_db")
    
    if not os.path.exists(vectorstore_dir):
        print("Database not found. Please run 'python src/ingest.py' first.")
        sys.exit(1)

    print("Connecting to ChromaDB...")
    # Initialize the same model to load the DB
    embeddings = HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    vectorstore = Chroma(
        persist_directory=vectorstore_dir,
        embedding_function=embeddings
    )
    
    # Get all documents from the collection
    collection = vectorstore._collection
    results = collection.get(include=["documents", "metadatas"])
    
    # Save them to a text file for easy reading
    export_path = os.path.join("data", "all_chunks_review.txt")
    os.makedirs("data", exist_ok=True)
    
    with open(export_path, "w", encoding="utf-8") as f:
        for i in range(len(results["ids"])):
            f.write(f"=== CHUNK {i+1} ===\n")
            f.write(f"Source URL: {results['metadatas'][i].get('source_url', 'Unknown')}\n")
            f.write(f"Length: {len(results['documents'][i])} characters\n")
            f.write(f"Text:\n{results['documents'][i]}\n\n")
            f.write("="*80 + "\n\n")
            
    print(f"Successfully exported {len(results['ids'])} chunks to {export_path}")
    print("You can now open that file to read exactly how the data was split!")

if __name__ == "__main__":
    main()

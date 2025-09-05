import chromadb

def add_text(text) -> None:
    """Add text to ChromaDB collection."""
    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection(name="my_collection")
    
    collection.upsert(
        documents=[text],
        ids=[f"doc_{len(collection.get()['ids']) + 1}"]
    )
    print(f"Added: {text}")

def search_text(query) -> list[str]:
    """Search for similar text in ChromaDB collection."""
    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection(name="my_collection")
    
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    print(results)
    result = results['documents'][0]
    return result
    

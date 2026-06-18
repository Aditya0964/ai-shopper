import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = "chroma_db"

_collection = None

def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        embedding_function = embedding_functions.DefaultEmbeddingFunction()
        _collection = client.get_collection(
            name="products",
            embedding_function=embedding_function
        )
    return _collection

def search_products_rag(query: str, k: int = 5) -> list:
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=k)
    
    products = []
    docs = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    
    for doc, metadata, distance in zip(docs, metadatas, distances):
        products.append({
            "product_id": metadata["product_id"],
            "name": metadata["name"],
            "price": float(metadata["price"]),
            "avg_rating": float(metadata["avg_rating"]),
            "image_url": metadata["image_url"],
            "relevance_score": round(1 - distance, 3),
            "description": doc
        })
    
    return products
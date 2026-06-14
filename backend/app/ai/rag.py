from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_PATH = "chroma_db"

def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma(
        collection_name="products",
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )

def search_products_rag(query: str, k: int = 5) -> list:
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search_with_score(query, k=k)
    
    products = []
    for doc, score in results:
        products.append({
            "product_id": doc.metadata["product_id"],
            "name": doc.metadata["name"],
            "price": float(doc.metadata["price"]),
            "avg_rating": float(doc.metadata["avg_rating"]),
            "image_url": doc.metadata["image_url"],
            "relevance_score": round(1 - score, 3),
            "description": doc.page_content
        })
    
    return products
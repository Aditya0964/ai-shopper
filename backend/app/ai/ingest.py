import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.product import Product
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_PATH = "chroma_db"

def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def ingest_products():
    print("Loading embedding model...")
    embeddings = get_embedding_model()

    print("Fetching products from MySQL...")
    db = SessionLocal()
    products = db.query(Product).filter(Product.is_active == True).all()
    db.close()
    print(f"Found {len(products)} products")

    print("Preparing documents...")
    texts = []
    metadatas = []
    ids = []

    for product in products:
        text = f"""Product: {product.name}
Price: ₹{product.price}
Rating: {product.avg_rating}
Description: {product.description or 'No description available'}"""

        texts.append(text)
        metadatas.append({
            "product_id": product.id,
            "name": product.name,
            "price": str(product.price),
            "avg_rating": str(product.avg_rating),
            "image_url": product.image_url or ""
        })
        ids.append(product.id)

    print("Embedding and storing in ChromaDB...")
    vectorstore = Chroma(
        collection_name="products",
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )

    batch_size = 100
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        batch_meta = metadatas[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        vectorstore.add_texts(
            texts=batch_texts,
            metadatas=batch_meta,
            ids=batch_ids
        )
        print(f"  Embedded {min(i+batch_size, len(texts))}/{len(texts)} products")

    print(f"\nIngestion complete — {len(texts)} products embedded into ChromaDB")

if __name__ == "__main__":
    ingest_products()
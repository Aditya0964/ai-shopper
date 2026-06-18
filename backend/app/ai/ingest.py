import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.product import Product
import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = "chroma_db"

def ingest_products():
    print("Setting up ChromaDB client...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    try:
        client.delete_collection("products")
        print("Deleted old collection")
    except Exception:
        pass

    collection = client.create_collection(
        name="products",
        embedding_function=embedding_function
    )

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
Price: Rs.{product.price}
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
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        batch_meta = metadatas[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        collection.add(
            documents=batch_texts,
            metadatas=batch_meta,
            ids=batch_ids
        )
        print(f"  Embedded {min(i+batch_size, len(texts))}/{len(texts)} products")

    print(f"\nIngestion complete — {len(texts)} products embedded into ChromaDB")

if __name__ == "__main__":
    ingest_products()
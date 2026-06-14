import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.product import Product, Category
from app.models.order import Review
import uuid

CSV_PATH = "amazon.csv"

def clean_price(price_str):
    if pd.isna(price_str):
        return 0.0
    cleaned = str(price_str).replace("₹", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except:
        return 0.0

def clean_rating(rating):
    try:
        return float(rating)
    except:
        return 0.0

def get_top_category(category_str):
    if pd.isna(category_str):
        return "General"
    return category_str.split("|")[0].strip()

def slugify(text):
    return text.lower()\
               .replace("&", "and")\
               .replace(" ", "-")\
               .replace("/", "-")\
               .replace(",", "")\
               .replace("(", "")\
               .replace(")", "")

def ingest():
    print("Reading CSV...")
    df = pd.read_csv(CSV_PATH)
    df = df.drop_duplicates(subset=["product_id"])
    print(f"Found {len(df)} unique products")

    db = SessionLocal()

    try:
        # Step 1 — Create categories
        print("\nCreating categories...")
        category_map = {}

        for _, row in df.iterrows():
            top_cat = get_top_category(row["category"])
            if top_cat not in category_map:
                slug = slugify(top_cat)
                existing = db.query(Category).filter(Category.slug == slug).first()
                if existing:
                    category_map[top_cat] = existing.id
                else:
                    cat = Category(
                        id=str(uuid.uuid4()),
                        name=top_cat,
                        slug=slug
                    )
                    db.add(cat)
                    db.commit()
                    db.refresh(cat)
                    category_map[top_cat] = cat.id
                    print(f"  Created category: {top_cat}")

        # Step 2 — Create products
        print("\nCreating products...")
        product_map = {}
        created = 0
        skipped = 0

        for _, row in df.iterrows():
            existing = db.query(Product).filter(
                Product.name == str(row["product_name"])
            ).first()

            if existing:
                product_map[row["product_id"]] = existing.id
                skipped += 1
                continue

            top_cat = get_top_category(row["category"])
            category_id = category_map.get(top_cat)
            price = clean_price(row["discounted_price"])
            if price == 0.0:
                price = clean_price(row["actual_price"])

            product = Product(
                id=str(uuid.uuid4()),
                name=str(row["product_name"])[:200],
                description=str(row["about_product"]) if pd.notna(row["about_product"]) else None,
                price=price,
                stock=100,
                image_url=str(row["img_link"]) if pd.notna(row["img_link"]) else None,
                avg_rating=clean_rating(row["rating"]),
                category_id=category_id
            )
            db.add(product)
            db.commit()
            db.refresh(product)
            product_map[row["product_id"]] = product.id
            created += 1

            if created % 50 == 0:
                print(f"  {created} products created...")

        print(f"  Done — {created} created, {skipped} skipped")

        # Step 3 — Create reviews
        print("\nCreating reviews...")
        review_count = 0

        for _, row in df.iterrows():
            product_id = product_map.get(row["product_id"])
            if not product_id:
                continue

            titles = str(row["review_title"]).split(",") if pd.notna(row["review_title"]) else []
            contents = str(row["review_content"]).split(",") if pd.notna(row["review_content"]) else []

            for i, title in enumerate(titles[:3]):
                content = contents[i] if i < len(contents) else ""
                review = Review(
                    id=str(uuid.uuid4()),
                    user_id="d149e1b0-5528-4eda-9317-40cef042a13a",
                    product_id=product_id,
                    rating=int(clean_rating(row["rating"])),
                    body=f"{title.strip()} — {content.strip()}"[:500]
                )
                db.add(review)
                review_count += 1

            if review_count % 100 == 0 and review_count > 0:
                db.commit()

        db.commit()
        print(f"  Done — {review_count} reviews created")

        print("\nIngestion complete!")
        print(f"Categories: {len(category_map)}")
        print(f"Products: {created}")
        print(f"Reviews: {review_count}")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    ingest()
from sqlalchemy.orm import Session
from app.models.product import Product, Category
from app.schemas.product import ProductCreate, ProductUpdate, CategoryCreate
import uuid


def get_all_categories(db: Session):
    return db.query(Category).all()


def create_category(db: Session, category: CategoryCreate):
    existing = db.query(Category).filter(Category.slug == category.slug).first()
    if existing:
        return None
    new_category = Category(
        id=str(uuid.uuid4()),
        name=category.name,
        slug=category.slug
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def get_all_products(db: Session, category_id: str = None, min_price: float = None, max_price: float = None):
    query = db.query(Product).filter(Product.is_active == True)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    return query.all()


def get_product_by_id(db: Session, product_id: str):
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product: ProductCreate):
    new_product = Product(
        id=str(uuid.uuid4()),
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        image_url=product.image_url,
        category_id=product.category_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def update_product(db: Session, product_id: str, updates: ProductUpdate):
    product = get_product_by_id(db, product_id)
    if not product:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: str):
    product = get_product_by_id(db, product_id)
    if not product:
        return None
    product.is_active = False
    db.commit()
    return product
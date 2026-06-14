from sqlalchemy.orm import Session
from app.models.order import CartItem
from app.models.product import Product
import uuid


def get_cart(db: Session, user_id: str):
    items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    result = []
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        result.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_name": product.name,
            "product_price": product.price,
            "image_url": product.image_url,
            "quantity": item.quantity,
            "subtotal": product.price * item.quantity
        })
    return result


def add_to_cart(db: Session, user_id: str, product_id: str, quantity: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None, "Product not found"
    if product.stock < quantity:
        return None, "Insufficient stock"

    existing = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    ).first()

    if existing:
        existing.quantity += quantity
        db.commit()
        db.refresh(existing)
        return existing, None
    
    new_item = CartItem(
        id=str(uuid.uuid4()),
        user_id=user_id,
        product_id=product_id,
        quantity=quantity
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item, None


def update_cart_item(db: Session, user_id: str, item_id: str, quantity: int):
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == user_id
    ).first()
    if not item:
        return None
    if quantity <= 0:
        db.delete(item)
        db.commit()
        return "deleted"
    item.quantity = quantity
    db.commit()
    db.refresh(item)
    return item


def remove_from_cart(db: Session, user_id: str, item_id: str):
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == user_id
    ).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def clear_cart(db: Session, user_id: str):
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()
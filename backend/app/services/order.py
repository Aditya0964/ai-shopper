from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem, CartItem
from app.models.product import Product
import uuid


def place_order(db: Session, user_id: str):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    if not cart_items:
        return None, "Cart is empty"

    total = 0
    order_items_data = []

    for cart_item in cart_items:
        product = db.query(Product).filter(
            Product.id == cart_item.product_id
        ).with_for_update().first()

        if not product:
            return None, f"Product not found"
        if product.stock < cart_item.quantity:
            return None, f"Insufficient stock for {product.name}"

        total += product.price * cart_item.quantity
        order_items_data.append({
            "product": product,
            "quantity": cart_item.quantity,
            "unit_price": product.price
        })

    order = Order(
        id=str(uuid.uuid4()),
        user_id=user_id,
        total_amount=total,
        status="pending"
    )
    db.add(order)

    for item_data in order_items_data:
        order_item = OrderItem(
            id=str(uuid.uuid4()),
            order_id=order.id,
            product_id=item_data["product"].id,
            quantity=item_data["quantity"],
            unit_price=item_data["unit_price"]
        )
        db.add(order_item)
        item_data["product"].stock -= item_data["quantity"]

    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()
    db.refresh(order)
    return order, None


def get_user_orders(db: Session, user_id: str):
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_order_by_id(db: Session, order_id: str, user_id: str):
    return db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()


def get_all_orders(db: Session):
    return db.query(Order).all()


def update_order_status(db: Session, order_id: str, status: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    order.status = status
    db.commit()
    db.refresh(order)
    return order
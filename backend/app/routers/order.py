from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.order import OrderResponse
from app.services import order as order_service
from app.services.dependencies import get_current_user, get_current_admin

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=201)
def place_order(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    order, error = order_service.place_order(db, current_user.id)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return order


@router.get("/", )
def get_my_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    orders = order_service.get_user_orders(db, current_user.id)
    result = []
    for order in orders:
        order_dict = {
            "id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "total_amount": order.total_amount,
            "payment_id": order.payment_id,
            "created_at": str(order.created_at),
            "order_items": [
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "product_name": item.product.name if item.product else item.product_id,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price
                }
                for item in order.order_items
            ]
        }
        result.append(order_dict)
    return result


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    order = order_service.get_order_by_id(db, order_id, current_user.id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/admin/all", response_model=List[OrderResponse])
def get_all_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    return order_service.get_all_orders(db)


@router.put("/admin/{order_id}/status")
def update_status(
    order_id: str,
    status: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    valid_statuses = ["pending", "paid", "shipped", "delivered", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")
    order = order_service.update_order_status(db, order_id, status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": f"Order status updated to {status}"}
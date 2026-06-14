from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import cart as cart_service
from app.services.dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/")
def get_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return cart_service.get_cart(db, current_user.id)


@router.post("/")
def add_to_cart(
    product_id: str,
    quantity: int = 1,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    item, error = cart_service.add_to_cart(db, current_user.id, product_id, quantity)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "Item added to cart", "item_id": item.id}


@router.put("/{item_id}")
def update_cart_item(
    item_id: str,
    quantity: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = cart_service.update_cart_item(db, current_user.id, item_id, quantity)
    if not result:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if result == "deleted":
        return {"message": "Item removed from cart"}
    return {"message": "Cart updated"}


@router.delete("/{item_id}")
def remove_from_cart(
    item_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    success = cart_service.remove_from_cart(db, current_user.id, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Item removed from cart"}


@router.delete("/")
def clear_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    cart_service.clear_cart(db, current_user.id)
    return {"message": "Cart cleared"}
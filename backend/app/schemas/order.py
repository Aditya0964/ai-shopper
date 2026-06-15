from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CartItemCreate(BaseModel):
    product_id: str
    quantity: int


class CartItemResponse(BaseModel):
    id: str
    product_id: str
    quantity: int

    class Config:
        from_attributes = True


class OrderItemResponse(BaseModel):
    id: str
    product_id: str
    quantity: int
    unit_price: float
    product_name: Optional[str] = None

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    items: List[CartItemCreate]


class OrderResponse(BaseModel):
    id: str
    user_id: str
    status: str
    total_amount: float
    payment_id: Optional[str]
    created_at: datetime
    order_items: List[OrderItemResponse]

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    rating: int
    body: Optional[str] = None


class ReviewResponse(BaseModel):
    id: str
    user_id: str
    product_id: str
    rating: int
    body: Optional[str]
    sentiment_score: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, CategoryCreate, CategoryResponse
from app.services import product as product_service
from app.services.dependencies import get_current_user, get_current_admin

router = APIRouter(prefix="/products", tags=["products"])
category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return product_service.get_all_categories(db)


@category_router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    created = product_service.create_category(db, category)
    if not created:
        raise HTTPException(status_code=400, detail="Category with this slug already exists")
    return created


@router.get("/")
def get_products(
    category_id: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return product_service.get_all_products(db, category_id, min_price, max_price, page, limit)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    return product_service.create_product(db, product)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    updates: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    updated = product_service.update_product(db, product_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@router.delete("/{product_id}")
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    deleted = product_service.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deactivated successfully"}
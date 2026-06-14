from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services import auth as auth_service
from app.models.user import User
from app.services.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    created = auth_service.create_user(db, user)
    if not created:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return created


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    verified = auth_service.verify_user(db, user.email, user.password)
    if not verified:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    token = auth_service.create_access_token({"sub": verified.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": verified.id,
            "name": verified.name,
            "email": verified.email
        }
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
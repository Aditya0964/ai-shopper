from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, product, cart, order

app = FastAPI(title="AI Shopper API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(product.router)
app.include_router(product.category_router)
app.include_router(cart.router)
app.include_router(order.router)


@app.get("/")
def root():
    return {"message": "AI Shopper API is running"}
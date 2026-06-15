# 🛍️ AI Shopper — AI-Powered Personal Shopping Assistant

A full-stack e-commerce web app with an intelligent shopping assistant powered by RAG, LangChain, and Google Gemini. Users can browse 1300+ real products, manage their cart and orders, and interact with an AI agent that understands natural language to find products, compare items, and add to cart automatically.

Some of the items may not have working image url, so the product image might not be there.
---

## 🚀 Live Demo

---

## ✨ Features

### 🛒 Core E-commerce
- User authentication with JWT (register, login, protected routes)
- Browse 1338+ real Amazon products across 9 categories
- Product detail pages with reviews and ratings
- Cart management (add, update quantity, remove)
- Order placement with automatic stock management

### 🤖 AI Layer
- **Natural language search** — "find me earphones under ₹1000" works perfectly
- **RAG pipeline** — product catalog embedded in ChromaDB, retrieved semantically
- **LangChain agent** with 5 tools: search, filter, get details, compare, add to cart
- **Floating chat widget** — available on every page when logged in
- Agent can take actions: "add the cheapest one to my cart" actually adds it

### 📊 ML
- Sentiment analysis scores on product reviews (scikit-learn)
- Review sentiment stored in database and displayed on product pages

---

## 🏗️ Architecture

```
Frontend (React + Vite + Tailwind)
         ↓ REST API
Backend (FastAPI + Python)
    ├── Auth service (JWT)
    ├── Product service
    ├── Cart service
    ├── Order service
    └── AI layer
         ├── RAG pipeline (LangChain + ChromaDB)
         ├── LangChain agent (tool calling)
         └── Google Gemini 2.5 Flash
         ↓
Data Layer
    ├── MySQL (users, products, orders, reviews)
    ├── ChromaDB (product embeddings)
    └── SQLAlchemy ORM + Alembic migrations
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, Tailwind CSS, Zustand, React Router |
| Backend | FastAPI, Python, SQLAlchemy, Alembic |
| Database | MySQL, ChromaDB |
| AI/LLM | Google Gemini 2.5 Flash, LangChain |
| RAG | sentence-transformers (all-MiniLM-L6-v2), ChromaDB |
| ML | scikit-learn (sentiment analysis) |
| Auth | JWT, OAuth2 |

---

## 📁 Project Structure

```
ai-shopper/
├── backend/
│   ├── app/
│   │   ├── ai/          # RAG pipeline + LangChain agent
│   │   ├── models/      # SQLAlchemy models
│   │   ├── routers/     # FastAPI endpoints
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   └── main.py
│   ├── alembic/         # DB migrations
│   └── requirements.txt
└── frontend/
    └── src/
        ├── components/  # Navbar, ProductCard, ChatWidget
        ├── pages/       # Home, Login, Register, Cart, Orders
        ├── api/         # Axios instance
        └── store/       # Zustand auth store
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11+
- Node.js 20+
- MySQL 8.0+

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Fill in DATABASE_URL, GOOGLE_API_KEY, SECRET_KEY

# Run migrations
alembic upgrade head

# Seed product data
python ingest_data.py

# Embed products into ChromaDB
python -m app.ai.ingest

# Start server
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /auth/register | Create account |
| POST | /auth/login | Login, get JWT |
| GET | /products/ | List products (paginated, filterable) |
| GET | /products/{id} | Product detail |
| GET | /categories/ | All categories |
| GET | /cart/ | Get cart |
| POST | /cart/ | Add to cart |
| POST | /orders/ | Place order |
| GET | /orders/ | Order history |
| POST | /chat/ | AI chat (natural language) |

---

## 🧠 How the AI Works

1. User types a natural language message in the chat widget
2. LangChain agent (powered by Gemini 2.5 Flash) decides which tools to call
3. `search_products` tool embeds the query and searches ChromaDB semantically
4. Retrieved products are injected into the LLM prompt as context (RAG)
5. LLM responds using only real products — no hallucination
6. Agent can chain tools: search → filter → add to cart in one conversation turn

---

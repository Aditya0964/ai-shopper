# 🛍️ AI Shopper — AI-Powered Personal Shopping Assistant

A full-stack e-commerce web app with an intelligent shopping assistant powered by RAG, LangChain, and Groq's Llama 3.3. Users can browse 1300+ real products, manage their cart and orders, and interact with an AI agent that understands natural language to find products, compare items, and add to cart automatically.

---

## 🚀 Live Demo

- **Frontend:** [ai-shopper-iota.vercel.app](https://ai-shopper-iota.vercel.app)
- **Backend API:** [ai-shopper.onrender.com](https://ai-shopper.onrender.com)

---

## ✨ Features

### 🛒 Core E-commerce
- User authentication with JWT (register, login, protected routes)
- Browse 1370+ real Amazon products across 9 categories
- Product detail pages with reviews and ratings
- Cart management (add, update quantity, remove)
- Order placement with automatic stock management

### 🤖 AI Layer
- **Natural language search** — "find me earphones under ₹1000" works perfectly
- **RAG pipeline** — product catalog embedded in ChromaDB, retrieved semantically
- **LangChain agent** with 5 tools: search, filter, get details, compare, add to cart
- **Floating chat widget** — available on every page when logged in
- Agent can take actions: "add the cheapest one to my cart" actually adds it
- Powered by Groq's Llama 3.3 70B for fast, reliable tool-calling

---

## 🏗️ Architecture

```
Frontend (React + Vite + Tailwind) — deployed on Vercel
         ↓ REST API
Backend (FastAPI + Python) — deployed on Render
    ├── Auth service (JWT)
    ├── Product service
    ├── Cart service
    ├── Order service
    └── AI layer
         ├── RAG pipeline (LangChain + ChromaDB)
         ├── LangChain agent (tool calling)
         └── Groq (Llama 3.3 70B)
         ↓
Data Layer
    ├── MySQL — Aiven (users, products, orders, reviews)
    ├── ChromaDB (product embeddings)
    └── SQLAlchemy ORM + Alembic migrations
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, Tailwind CSS, Zustand, React Router |
| Backend | FastAPI, Python, SQLAlchemy, Alembic |
| Database | MySQL (Aiven), ChromaDB |
| AI/LLM | Groq (Llama 3.3 70B), LangChain |
| RAG | sentence-transformers (all-MiniLM-L6-v2), ChromaDB |
| Auth | JWT, OAuth2 |
| Deployment | Vercel (frontend), Render (backend), Aiven (database) |

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
│   ├── chroma_db/       # Pre-embedded product vectors
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
- MySQL 8.0+ (or an Aiven/cloud MySQL instance)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Fill in DATABASE_URL, GROQ_API_KEY, SECRET_KEY

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
| GET | /auth/me | Get current user |
| GET | /products/ | List products (paginated, filterable) |
| GET | /products/{id} | Product detail |
| GET | /products/{id}/reviews | Product reviews |
| GET | /categories/ | All categories |
| GET | /cart/ | Get cart |
| POST | /cart/ | Add to cart |
| PUT | /cart/{id} | Update cart item quantity |
| DELETE | /cart/{id} | Remove cart item |
| POST | /orders/ | Place order |
| GET | /orders/ | Order history |
| POST | /chat/ | AI chat (natural language) |

---

## 🧠 How the AI Works

1. User types a natural language message in the chat widget
2. LangChain agent (powered by Groq's Llama 3.3 70B) decides which tools to call
3. `search_products` tool embeds the query and searches ChromaDB semantically
4. Retrieved products are injected into the LLM prompt as context (RAG)
5. LLM responds using only real products — no hallucination
6. Agent can chain tools: search → filter → add to cart in one conversation turn

---

## 🔐 Security Notes

- Passwords, API keys, and database credentials are never committed (`.env` is gitignored)
- `alembic.ini` (containing DB credentials) is gitignored — use `alembic.ini.example` as a template
- JWT tokens expire after 24 hours
- CORS is restricted to known frontend origins

---

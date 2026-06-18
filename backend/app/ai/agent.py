import os
import uuid
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from app.ai.rag import search_products_rag
from app.database import SessionLocal
from app.models.product import Product
from app.models.order import CartItem

load_dotenv()


def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )


@tool
def search_products(query: str) -> str:
    """Search for products using natural language query.
    Use this when user asks to find, search, or show products."""
    results = search_products_rag(query, k=5)
    if not results:
        return "No products found for this query."
    response = f"Found {len(results)} relevant products:\n\n"
    for i, p in enumerate(results, 1):
        response += f"{i}. {p['name'][:80]}\n"
        response += f"   Price: ₹{p['price']} | Rating: {p['avg_rating']} | ID: {p['product_id']}\n\n"
    return response


@tool
def filter_products(max_price: float = None, min_price: float = None, min_rating: float = None) -> str:
    """Filter products by price range or minimum rating.
    Use this when user specifies a budget or rating requirement."""
    db = SessionLocal()
    try:
        query = db.query(Product).filter(Product.is_active == True)
        if max_price:
            query = query.filter(Product.price <= max_price)
        if min_price:
            query = query.filter(Product.price >= min_price)
        if min_rating:
            query = query.filter(Product.avg_rating >= min_rating)
        products = query.limit(5).all()
        if not products:
            return "No products found matching these filters."
        response = f"Found products matching filters:\n\n"
        for i, p in enumerate(products, 1):
            response += f"{i}. {p.name[:80]}\n"
            response += f"   Price: ₹{p.price} | Rating: {p.avg_rating} | ID: {p.id}\n\n"
        return response
    finally:
        db.close()


@tool
def get_product_details(product_id: str) -> str:
    """Get full details of a specific product by its ID."""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return "Product not found."
        return f"""Name: {product.name}
Price: ₹{product.price}
Rating: {product.avg_rating}
Stock: {product.stock}
Description: {product.description[:300] if product.description else 'No description'}"""
    finally:
        db.close()


@tool
def add_to_cart(product_id: str, user_id: str, quantity: int = 1) -> str:
    """Add a product to the user's cart."""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return "Product not found."
        if product.stock < quantity:
            return f"Insufficient stock. Only {product.stock} available."
        existing = db.query(CartItem).filter(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id
        ).first()
        if existing:
            existing.quantity += quantity
        else:
            cart_item = CartItem(
                id=str(uuid.uuid4()),
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )
            db.add(cart_item)
        db.commit()
        return f"Successfully added {quantity}x '{product.name[:50]}' to cart!"
    finally:
        db.close()
        
@tool
def compare_products(product_id_1: str, product_id_2: str) -> str:
    """Compare two products side by side."""
    db = SessionLocal()
    try:
        p1 = db.query(Product).filter(Product.id == product_id_1).first()
        p2 = db.query(Product).filter(Product.id == product_id_2).first()
        if not p1 or not p2:
            return "One or both products not found."
        return f"""Comparison:

{p1.name[:60]}
  Price: ₹{p1.price} | Rating: {p1.avg_rating} | Stock: {p1.stock}

{p2.name[:60]}
  Price: ₹{p2.price} | Rating: {p2.avg_rating} | Stock: {p2.stock}

Price difference: ₹{abs(p1.price - p2.price):.2f}
Better rated: {p1.name[:30] if p1.avg_rating >= p2.avg_rating else p2.name[:30]}
Cheaper: {p1.name[:30] if p1.price <= p2.price else p2.name[:30]}"""
    finally:
        db.close()


def run_agent(user_message: str, user_id: str) -> str:
    llm = get_llm()
    tools = [search_products, filter_products, get_product_details, add_to_cart, compare_products]
    llm_with_tools = llm.bind_tools(tools)

    system_prompt = f"""You are a helpful AI shopping assistant for an online store.
        You help users find products, compare them, and manage their cart.

        When showing products, ALWAYS use this exact format for each product:
        🔹 **Product Name**
        💰 Price: ₹X | ⭐ Rating: X | ID: xxx

        Keep responses concise and friendly.
        The current user's ID is: {user_id}
        When adding to cart, always use this user_id."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]

    print(f"\nUser: {user_message}")

    while True:
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            content = response.content
            if isinstance(content, list):
                content = " ".join([c["text"] for c in content if isinstance(c, dict) and "text" in c])
            print(f"Assistant: {content}")
            return content

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            print(f"\nCalling tool: {tool_name} with {tool_args}")

            tool_map = {t.name: t for t in tools}
            tool_result = tool_map[tool_name].invoke(tool_args)
            print(f"Tool result: {str(tool_result)[:200]}...")

            from langchain_core.messages import ToolMessage
            messages.append(ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            ))
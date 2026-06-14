from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.services.dependencies import get_current_user
from app.ai.agent import run_agent

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatMessage(BaseModel):
    message: str


@router.post("/")
def chat(
    body: ChatMessage,
    current_user=Depends(get_current_user)
):
    response = run_agent(body.message, current_user.id)
    return {
        "message": body.message,
        "response": response,
        "user_id": current_user.id
    }
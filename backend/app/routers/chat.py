from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.function_calling import handle_chat

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

# openaiとのチャット用
@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    reply = await handle_chat(request.message, db)
    return {"reply": reply}

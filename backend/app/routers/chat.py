from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

router = APIRouter()

# .envの読み込み
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("prompts/prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

class ChatRequest(BaseModel):
    message: str

# openaiとのチャット用
@router.post("/chat")
async def chat(request: ChatRequest):
#     使わない時はコメントアウト〜ここから
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": request.message},
        ],
    )
    return {"reply": response.choices[0].message.content}
#     使わない時はコメントアウト〜ここまで

#     return {"reply": f"受け取ったメッセージ: {request.message}"}

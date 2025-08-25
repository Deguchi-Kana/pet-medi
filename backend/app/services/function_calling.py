from openai import OpenAI
from app.crud.schedule import get_schedule_by_pet_id
from app.crud.pet import get_pet_id_by_name
from sqlalchemy.orm import Session
import os, json
from dotenv import load_dotenv
from pathlib import Path

# .envの読み込み
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("prompts/pet.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

async def handle_chat(message_text: str, db: Session):
    functions = [
        {
            "name": "get_pet_id_by_name",
            "description": "ペットの名前からIDを取得する",
            "parameters": {
                "type": "object",
                "properties": {"name": {"type": "string", "description": "ペットの名前"}},
                "required": ["name"]
            }
        },
        {
            "name": "get_schedule_by_pet_id",
            "description": "ペットIDから投薬スケジュールを取得する",
            "parameters": {
                "type": "object",
                "properties": {"pet_id": {"type": "integer", "description": "ペットID"}},
                "required": ["pet_id"]
            }
        }
    ]

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": message_text}],
        functions=functions,
        function_call="auto"
    )

    message = response.choices[0].message

    if message.function_call:
        func_name = message.function_call.name
        args = json.loads(message.function_call.arguments)

        if func_name == "get_pet_id_by_name":
            pet_id = get_pet_id_by_name(db, **args)
            if not pet_id:
                return "データがありません。"
            schedule = get_schedule_by_pet_id(db, pet_id)
            final_resp = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message_text},
                    {"role": "function", "name": func_name, "content": json.dumps({"pet_id": pet_id})},
                    {"role": "function", "name": "get_schedule_by_pet_id", "content": json.dumps(schedule)}
                ]
            )
            return final_resp.choices[0].message.content

    return "質問を理解できませんでした。"

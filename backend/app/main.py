from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from .schemas import MedicineCreate

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}

@app.post("/medicines")
def create_medicine(medicine: MedicineCreate):
    print("受け取ったデータ:", medicine)
    return {"message": "登録成功", "data": medicine}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番では制限する
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

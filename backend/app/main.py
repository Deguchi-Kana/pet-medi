from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.schemas import MedicineCreate
from app.database import engine, get_db
from app.models.medicine import Medicine, Base
from app.routers import medicine

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}

@app.post("/medicines")
def create_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    db_medicine = Medicine(
        name=medicine.name,
        dosage=medicine.dosage,
    )
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return {
        "message": "登録成功",
        "data": {
            "id": db_medicine.id,
            "name": db_medicine.name,
            "dosage": db_medicine.dosage,
        }
    }

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(medicine.router)
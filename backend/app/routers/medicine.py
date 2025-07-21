from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud

router = APIRouter()

@router.post("/medicines")
def create_medicine(medicine: schemas.MedicineCreate, db: Session = Depends(get_db)):
    return crud.medicine.create_medicine(db, medicine)

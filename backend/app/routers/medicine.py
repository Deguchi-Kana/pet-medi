# backend/app/routers/medicine.py
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.medicine import MedicineCreate, MedicineOut
from app.crud import medicine as crud_medicine

router = APIRouter()

@router.get("/medicines", response_model=list[MedicineOut])
def get_medicines(db: Session = Depends(get_db)):
    medicines = crud_medicine.get_medicines(db)
    return [
        MedicineOut(
            id=m.id,
            name=m.name,
            dosage=m.dosage,
            notify=m.notify,
            timing=m.timing.split(",") if m.timing else [],
            pet_id=m.pet_id,
            start_date=m.start_date,
            duration_days=m.duration_days,
        )
        for m in medicines
    ]

@router.post("/medicines", response_model=MedicineOut)
def create_medicine(medicine: MedicineCreate = Body(...), db: Session = Depends(get_db)):
    db_medicine = crud_medicine.create_medicine(db, medicine)
    return MedicineOut(
        id=db_medicine.id,
        name=db_medicine.name,
        dosage=db_medicine.dosage,
        notify=db_medicine.notify,
        timing=db_medicine.timing.split(",") if db_medicine.timing else [],
        pet_id=db_medicine.pet_id,
        start_date=db_medicine.start_date,
        duration_days=db_medicine.duration_days,
    )

@router.put("/medicines/{medicine_id}", response_model=MedicineOut)
def update_medicine(medicine_id: int, medicine: MedicineCreate, db: Session = Depends(get_db)):
    db_medicine = crud_medicine.update_medicine(db, medicine_id, medicine)
    if not db_medicine:
        raise HTTPException(status_code=404, detail="薬が見つかりません")
    return MedicineOut(
        id=db_medicine.id,
        name=db_medicine.name,
        dosage=db_medicine.dosage,
        notify=db_medicine.notify,
        timing=db_medicine.timing.split(",") if db_medicine.timing else [],
        pet_id=db_medicine.pet_id,
        start_date=db_medicine.start_date,
        duration_days=db_medicine.duration_days,
    )

@router.delete("/medicines/{medicine_id}")
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    medicine = crud_medicine.delete_medicine(db, medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="薬が見つかりません")
    return {"message": "削除完了！"}

@router.get("/medicines/schedule")
def get_schedule(db: Session = Depends(get_db)):
    return crud_medicine.get_schedule(db)

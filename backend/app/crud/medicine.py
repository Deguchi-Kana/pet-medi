from sqlalchemy.orm import Session
from app.models.medicine import Medicine
from app.schemas.medicine import MedicineCreate
import datetime

def get_medicines(db: Session):
    return db.query(Medicine).all()

def create_medicine(db: Session, medicine: MedicineCreate):
    db_medicine = Medicine(
        name=medicine.name,
        dosage=medicine.dosage,
        notify=medicine.notify,
        timing=",".join(medicine.timing),
        pet_id=medicine.pet_id,
        start_date=medicine.start_date,
        duration_days=medicine.duration_days,
    )
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine

def update_medicine(db: Session, medicine_id: int, medicine: MedicineCreate):
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if db_medicine:
        db_medicine.name = medicine.name
        db_medicine.dosage = medicine.dosage
        db_medicine.notify = medicine.notify
        db_medicine.timing = ",".join(medicine.timing)
        db_medicine.start_date = medicine.start_date
        db_medicine.duration_days = medicine.duration_days
        db.commit()
        db.refresh(db_medicine)
    return db_medicine

def delete_medicine(db: Session, medicine_id: int):
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if medicine:
        db.delete(medicine)
        db.commit()
    return medicine

def get_schedule(db: Session):
    medicines = db.query(Medicine).all()
    schedule = []
    for medicine in medicines:
        if medicine.start_date and medicine.duration_days:
            for i in range(medicine.duration_days):
                day = medicine.start_date + datetime.timedelta(days=i)
                schedule.append({
                    "date": day.strftime("%Y-%m-%d"),
                    "name": medicine.name,
                    "timing": medicine.timing.split(",")
                })
    return schedule

from sqlalchemy.orm import Session
from app.models.medicine import Medicine
from app.models.pet import Pet
import datetime


def get_schedule(db: Session):
    medicines = db.query(Medicine).all()
    schedule = []

    for med in medicines:
        pet = db.query(Pet).filter(Pet.id == med.pet_id).first()
        if not pet or not med.start_date or not med.duration_days:
            continue
        for i in range(med.duration_days):
            day = med.start_date + datetime.timedelta(days=i)
            schedule.append({
                "date": day.strftime("%Y-%m-%d"),
                "medicine_name": med.name,
                "timing": med.timing.split(",") if med.timing else [],
                "pet_id": pet.id,
                "pet_name": pet.name,
                "dosage": med.dosage,
                "notify": med.notify,
            })
    return schedule

def get_schedule_by_pet_id(db: Session, pet_id: int):
    medicines = db.query(Medicine).filter(Medicine.pet_id == pet_id).all()
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
    return  sorted(schedule, key=lambda x: x["date"])

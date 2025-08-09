from fastapi import FastAPI, Depends, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.schemas import MedicineCreate
from app.schemas import MedicineOut
from app.schemas import PetOut
from app.schemas import PetCreate
from app.database import engine, get_db
from app.models.medicine import Medicine, Base
from app.models.pet import Pet, Base
from app.routers import medicine
from app.routers import pet
import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}

# 薬の一覧取得
@app.get("/medicines", response_model=list[MedicineOut])
def get_medicines(db: Session = Depends(get_db)):
    medicines = db.query(Medicine).all()

    # timingを文字列からList[str]に変換して整形
    result = []
    for m in medicines:
        result.append(MedicineOut(
            id=m.id,
            name=m.name,
            dosage=m.dosage,
            notify=m.notify,
            timing=m.timing.split(",") if m.timing else [],
            pet_id=m.pet_id,
            start_date=m.start_date,
            duration_days=m.duration_days,
        ))
    return result

# 薬の登録
@app.post("/medicines", response_model=MedicineCreate)
def create_medicine(medicine: MedicineCreate = Body(...), db: Session = Depends(get_db)):
    db_medicine = Medicine(
        name=medicine.name,
        dosage=medicine.dosage,
        notify=medicine.notify,
        timing=",".join(medicine.timing),
        pet_id=medicine.pet_id,
        start_date=medicine.start_date,
        duration_days=medicine.duration_days,
    )
    print("db_medicineオブジェクト:", db_medicine)
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    print("データベースにデータが登録されました")
    return MedicineCreate(
        id=db_medicine.id,
        pet_id=db_medicine.pet_id,
        name=db_medicine.name,
        dosage=db_medicine.dosage,
        notify=db_medicine.notify,
        timing=db_medicine.timing.split(",") if db_medicine.timing else [],
        start_date=db_medicine.start_date,
        duration_days=db_medicine.duration_days,
    )

# 薬の更新
@app.put("/medicines/{medicine_id}", response_model=MedicineCreate)
def update_medicine(medicine_id: int, medicine: MedicineCreate = Body(...), db: Session = Depends(get_db)):
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not db_medicine:
        raise HTTPException(status_code=404, detail="薬が見つかりません")
    db_medicine.name = medicine.name
    db_medicine.dosage = medicine.dosage
    db_medicine.notify = medicine.notify
    db_medicine.timing = ",".join(medicine.timing)
    db_medicine.start_date = medicine.start_date
    db_medicine.duration_days = medicine.duration_days
    db.commit()
    db.refresh(db_medicine)
    return MedicineCreate(
        id=db_medicine.id,
        pet_id=db_medicine.pet_id,
        name=db_medicine.name,
        dosage=db_medicine.dosage,
        notify=db_medicine.notify,
        timing=db_medicine.timing.split(",") if db_medicine.timing else [],
        start_date=db_medicine.start_date,
        duration_days=db_medicine.duration_days,
    )

# 薬の削除
@app.delete("/medicines/{medicine_id}")
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="薬が見つかりません")
    db.delete(medicine)
    db.commit()
    return {"message": "削除完了！"}

# 投薬スケジュールを取得
@app.get("/medicines/schedule")
def get_medicine_schedule(db: Session = Depends(get_db)):
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

# ペットの一覧取得
@app.get("/pets", response_model=list[PetOut])
def get_pets(db: Session = Depends(get_db)):
    pets = db.query(Pet).all()
    return pets

# ペットの登録
@app.post("/pets", response_model=PetOut)
def create_pet(pet: PetCreate=Body(...), db: Session = Depends(get_db)):
    db_pet = Pet(
        name=pet.name,
        species=pet.species,
        birthdate=pet.birthdate,
    )
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return PetOut(
        id=db_pet.id,
        name=db_pet.name,
        species=db_pet.species,
        birthdate=db_pet.birthdate,
    )

# ペットの更新
@app.put("/pets/{pet_id}", response_model=PetOut)
def update_pet(pet_id: int, pet: PetCreate=Body(...), db: Session = Depends(get_db)):
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="ペットが見つかりません")
    db_pet.name = pet.name
    db_pet.species = pet.species
    db_pet.birthdate = pet.birthdate
    db.commit()
    db.refresh(db_pet)
    return PetOut(
        id=db_pet.id,
        name=db_pet.name,
        species=db_pet.species,
        birthdate=db_pet.birthdate,
    )

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
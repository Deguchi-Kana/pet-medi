from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.pet import PetCreate, PetOut
from app.crud import pet as crud_pet

router = APIRouter()

@router.get("/pets", response_model=list[PetOut])
def get_pets(db: Session = Depends(get_db)):
    return crud_pet.get_pets(db)

@router.post("/pets", response_model=PetOut)
def create_pet(pet: PetCreate, db: Session = Depends(get_db)):
    return crud_pet.create_pet(db, pet)

@router.put("/pets/{pet_id}", response_model=PetOut)
def update_pet(pet_id: int, pet: PetCreate, db: Session = Depends(get_db)):
    db_pet = crud_pet.update_pet(db, pet_id, pet)
    if not db_pet:
        raise HTTPException(status_code=404, detail="ペットが見つかりません")
    return db_pet

@router.delete("/pets/{pet_id}")
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = crud_pet.delete_pet(db, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="ペットが見つかりません")
    return {"message": "削除完了！"}

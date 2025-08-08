from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud

router = APIRouter()

@router.post("/pets")
def create_pet(pet: schemas.PetCreate, db: Session = Depends(get_db)):
    return crud.pet.create_pet(db, pet)
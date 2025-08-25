from sqlalchemy.orm import Session
from app.models.pet import Pet
from app.schemas.pet import PetCreate

def get_pets(db: Session):
    return db.query(Pet).all()

def create_pet(db: Session, pet: PetCreate):
    db_pet = Pet(
        name=pet.name,
        species=pet.species,
        birthdate=pet.birthdate,
    )
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

def update_pet(db: Session, pet_id: int, pet: PetCreate):
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if db_pet:
        db_pet.name = pet.name
        db_pet.species = pet.species
        db_pet.birthdate = pet.birthdate
        db.commit()
        db.refresh(db_pet)
    return db_pet

def delete_pet(db: Session, pet_id: int):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if pet:
        db.delete(pet)
        db.commit()
    return pet

def get_pet_id_by_name(db: Session, name: str):
    pet = db.query(Pet).filter(Pet.name == name).first()
    return pet.id if pet else None

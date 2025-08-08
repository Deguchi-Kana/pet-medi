from pydantic import BaseModel
from datetime import date
from typing import Optional

# ペットの一覧取得
class PetOut(BaseModel):
    id: int
    name: str
    species: str
    birthdate: date

    class Config:
        from_attributes = True

# ペットの登録
class PetCreate(BaseModel):
    id: Optional[int] = None
    name: str
    species: str
    birthdate: date

class Pet(BaseModel):
    id: int
    name: str
    species: str
    birthdate: date

    class Config:
        orm_mode = True
from pydantic import BaseModel
from datetime import date
from typing import List, Optional


class MedicineCreate(BaseModel):
    name: str
    dosage: str
    timing: List[str]
    notify: bool
    pet_id: int

class Medicine(MedicineCreate):
    id: int

    class Config:
        orm_mode = True

# backend/app/schemas/schedule.py
from pydantic import BaseModel
from datetime import date
from typing import List
from .pet import PetOut

class MedicineEntry(BaseModel):
    pet: PetOut
    medicine_name: str
    timing: List[str]

class ScheduleByDate(BaseModel):
    date: date
    entries: List[MedicineEntry]

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import List

class ScheduleItem(BaseModel):
    date: str
    medicine_name: str
    timing: List[str]
    pet_id: int
    pet_name: str
    dosage: str
    notify: bool

    class Config:
        orm_mode = True

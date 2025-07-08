from pydantic import BaseModel
from typing import Optional, List

class MedicineCreate(BaseModel):
    name: str
    amount: str
    timing: List[str]
    notify: bool

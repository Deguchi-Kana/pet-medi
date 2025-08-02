from pydantic import BaseModel
from datetime import date
from typing import List, Optional


# 薬の一覧取得
class MedicineOut(BaseModel):
    id: int
    pet_id: int
    name: str
    dosage: str
    timing: List[str]
    notify: bool

    class Config:
        from_attributes = True

# 薬の登録
class MedicineCreate(BaseModel):
    id: Optional[int] = None
    pet_id: int
    name: str
    dosage: str
    timing: List[str]
    notify: bool

class Medicine(MedicineCreate):
    id: int

    class Config:
        orm_mode = True

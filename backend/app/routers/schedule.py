from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.schedule import get_schedule

router = APIRouter()

@router.get("/schedule")
def read_schedule(db: Session = Depends(get_db)):
    return get_schedule(db)

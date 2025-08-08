from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"))
    pet = relationship("Pet", back_populates="medicines")
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=True)
    timing = Column(String, nullable=True)
    notify = Column(Boolean, default=False)
    start_date = Column(DateTime, nullable=True)
    duration_days = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

from sqlalchemy import Column, Integer, String
from app.database import Base

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=True)
    timing = Column(String, nullable=True)

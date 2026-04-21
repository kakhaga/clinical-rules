from sqlalchemy import Column, Integer, String, Date
from app.db.base import Base

class Patient(Base):
    __tablename__ = "patients"
    __table_args__ = {"schema": "core"}

    id = Column(Integer, primary_key=True, index=True)
    external_patient_id = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)
    phone = Column(String)
    language = Column(String)
    pcp_provider_id = Column(Integer)
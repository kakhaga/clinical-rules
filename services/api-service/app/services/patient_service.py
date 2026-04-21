from sqlalchemy.orm import Session
from app.models.patient import Patient
from typing import Optional

def get_patients(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    last_name: Optional[str] = None,
    external_id: Optional[str] = None
):
    query = db.query(Patient)
    
    if last_name:
        query = query.filter(Patient.last_name.ilike(f"%{last_name}%"))
    if external_id:
        query = query.filter(Patient.external_patient_id == external_id)
        
    return query.offset(skip).limit(limit).all()

def get_patient_by_id(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()
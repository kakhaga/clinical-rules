from sqlalchemy.orm import Session
from sqlalchemy import case, and_, or_
from app.models.patient_evaluation_needs import PatientEvaluationNeeds
from typing import Optional

def get_patients_evaluation_needs(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    program_name: Optional[str] = None,
    specialty_need_name: Optional[str] = None,
    task_type: Optional[str] = None
):
   
    query = db.query(PatientEvaluationNeeds)

    # 3. Apply Filters
    if program_name:
        query = query.filter(PatientEvaluationNeeds.program_name == program_name)

    if specialty_need_name:
        query = query.filter(PatientEvaluationNeeds.specialty_need_name == specialty_need_name)
    
    if task_type:
        query = query.filter(PatientEvaluationNeeds.task_type == task_type)

    # 4. Apply Pagination (This now works perfectly!)
    return query.offset(skip).limit(limit).all()

def get_patient_evaluation_need_by_patient_id(db: Session, patient_id: int):
    return db.query(PatientEvaluationNeeds).filter(PatientEvaluationNeeds.patient_id == patient_id).all()


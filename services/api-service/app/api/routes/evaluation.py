from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.patient_evaluation_needs import PatientEvaluationNeedsOut 
from app.services import patient_evaluation_needs_service

router = APIRouter()

@router.get("/", response_model=List[PatientEvaluationNeedsOut])
def read_patients(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    program_name: Optional[str] = Query(None),
    specialty_need_name: Optional[str] = Query(None),
    task_type: Optional[str] = Query(None)
):
    """
    Retrieve patients with optional filtering.
    """
    return patient_evaluation_needs_service.get_patients_evaluation_needs(
        db, skip=skip, limit=limit, program_name=program_name, specialty_need_name=specialty_need_name, task_type=task_type
    )


@router.get("/{patient_id}", response_model=List[PatientEvaluationNeedsOut])
def read_patient_by_id(
    patient_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific patient by their primary key ID.
    """
    patient_needs = patient_evaluation_needs_service.get_patient_evaluation_need_by_patient_id(db, patient_id=patient_id)

    if not patient_needs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with id {patient_id} not found"
        )
    return patient_needs

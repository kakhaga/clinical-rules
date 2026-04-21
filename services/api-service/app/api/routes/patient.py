from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.patient import PatientOut
from app.services import patient_service

router = APIRouter()

@router.get("/", response_model=List[PatientOut])
def read_patients(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    last_name: Optional[str] = Query(None),
    external_id: Optional[str] = Query(None)
):
    """
    Retrieve patients with optional filtering.
    """
    patients = patient_service.get_patients(
        db, skip=skip, limit=limit, last_name=last_name, external_id=external_id
    )
    return patients

@router.get("/{patient_id}", response_model=PatientOut)
def read_patient_by_id(
    patient_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific patient by their primary key ID.
    """
    patient = patient_service.get_patient_by_id(db, patient_id=patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with id {patient_id} not found"
        )
    return patient

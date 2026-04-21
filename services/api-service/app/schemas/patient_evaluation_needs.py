from pydantic import BaseModel, ConfigDict, computed_field
from datetime import date
from typing import Optional

class PatientEvaluationNeedsOut(BaseModel):
    row_id: int
    patient_id: int  
    program_name: Optional[str]
    tier_name: Optional[str]
    previous_specialty_encounter: Optional[str]
    specialty_need_name: Optional[str]
    needs: Optional[str]
    encounter_date: Optional[date]
    last_evaluated_at: Optional[date]
    days_since_last_evaluation: Optional[int]
    cadence_days: Optional[int]
    task_type: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class PatientOut(BaseModel):
    id: int
    external_patient_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Optional[str]
    phone: Optional[str]
    language: Optional[str]
    pcp_provider_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)
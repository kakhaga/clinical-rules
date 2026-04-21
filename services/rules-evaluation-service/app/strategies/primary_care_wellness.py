from typing import List

from .base import ClinicalProgramStrategy
from app.models.patient_diagnosis import PatientDiagnosisView
from app.models.evaluation_result import EvaluationResult
from datetime import datetime, date

class PrimaryCareWellnessStrategy(ClinicalProgramStrategy):
    @property
    def name(self):
        return "Primary Care Wellness"

    def is_eligible(self, patient: PatientDiagnosisView) -> bool:
        today = date.today()
        birthdate = patient.date_of_birth
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age >= 18

    def evaluate(self, patient: PatientDiagnosisView) -> List[EvaluationResult]:
        result = EvaluationResult()
        result.patient_id = patient.id
        result.program_name = self.name
        result.eligible = True
        result.evaluated_at = patient.diagnosed_date
        
        result.specialty = "PCP"

        result.risk_tier = "Standard"
        result.needs = "visit every 180 days"

        if patient.icd_code_ref is not None:
            result.risk_tier = "High Priority"
            result.needs = "visit every 365 days"

        
        return [result, ]
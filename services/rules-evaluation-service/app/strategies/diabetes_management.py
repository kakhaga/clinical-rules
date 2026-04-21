from typing import List

from .base import ClinicalProgramStrategy
from app.models.patient_diagnosis import PatientDiagnosisView
from app.models.evaluation_result import EvaluationResult
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import copy

class DiabetesManagementStrategy(ClinicalProgramStrategy):
    @property
    def name(self):
        return "Diabetes Management"

    def is_eligible(self, patient: PatientDiagnosisView) -> bool:
        return patient.icd_family in ("E10", "E11")

    def evaluate(self, patient: PatientDiagnosisView) -> List[EvaluationResult]:
        result = EvaluationResult()
        result.patient_id = patient.id
        result.program_name = self.name
        result.eligible = True
        result.evaluated_at = patient.diagnosed_date

        diff = relativedelta(datetime.now(), patient.diagnosed_date)
        total_months_since_last_diagnosed = (diff.years * 12) + diff.months

        specialty_needs_dict = {}

        if 'a1c' in patient.test_name.lower() and total_months_since_last_diagnosed <= 6:
            if patient.result_value >= 9:
                result.risk_tier = "High Risk"
                specialty_needs_dict["Endocrinology"] = "every 90 days"
                specialty_needs_dict["Cardiology"] = "every 90 days"
                specialty_needs_dict["Podiatry"] = "every 180 days"
                specialty_needs_dict["Ophthalmology"] = "every 365 days"
                specialty_needs_dict["Nephrology"] = "every 180 days"

            elif patient.result_value >= 7 and patient.result_value < 9:
                result.risk_tier = "Moderate Risk"
                specialty_needs_dict["Endocrinology"] = "every 180 days"
                specialty_needs_dict["Podiatry"] = "every 365 days"
                specialty_needs_dict["Ophthalmology"] = "every 365 days"
            else:
                result.risk_tier = "Low Risk"
                specialty_needs_dict["Endocrinology"] = "every 365 days"
                specialty_needs_dict["Ophthalmology"] = "every 365 days"

        else:
            result.risk_tier = "Unmonitored"
            specialty_needs_dict["Endocrinology"] = "every 90 days (priority: get labs done)"

        evaluation_results = []

        for key,val in specialty_needs_dict.items():
            new_result = copy.deepcopy(result)
            new_result.specialty = key
            new_result.needs = val
            evaluation_results.append(new_result)
        
        
        return evaluation_results
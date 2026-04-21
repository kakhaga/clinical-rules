from abc import ABC, abstractmethod
from typing import List
from app.models.patient_diagnosis import PatientDiagnosisView
from app.models.evaluation_result import EvaluationResult

class ClinicalProgramStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def is_eligible(self, patient: PatientDiagnosisView) -> bool:
        pass

    @abstractmethod
    def evaluate(self, patient: PatientDiagnosisView) -> List[EvaluationResult]:
        pass
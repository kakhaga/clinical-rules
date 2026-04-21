from typing import List

from app.strategies.base import ClinicalProgramStrategy
from app.models.patient_diagnosis import PatientDiagnosisView
from app.models.evaluation_result import EvaluationResult

class RulesEngine:
    def __init__(self, strategies: List[ClinicalProgramStrategy]):
        self.strategies = strategies

    def process_patient(self, patient: PatientDiagnosisView) -> List[EvaluationResult]:
        results = []
        
        for strategy in self.strategies:
            # We wrap in a try-block to ensure one failing strategy 
            # doesn't crash the entire evaluation for other programs
            try:
                if strategy.is_eligible(patient):
                    result = strategy.evaluate(patient)
                    results.extend(result)
            except Exception as e:
                # Log error and continue to next strategy
                print(f"Error evaluating {strategy.__class__.__name__}: {e}")
                
        return results

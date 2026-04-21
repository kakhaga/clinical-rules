from typing import Dict, List

from app.models.patient_diagnosis import PatientDiagnosisView
from app.models.evaluation_result import EvaluationResult
from app.models.care.patient_evaluation import PatientEvaluation
from app.db import session
from app.services.engine import RulesEngine

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func

from app.strategies.diabetes_management import DiabetesManagementStrategy
from app.strategies.primary_care_wellness import PrimaryCareWellnessStrategy
import json


class EvaluationService:

    def cache_dimension_lookups(self, db):
        from app.models.care.program import DimProgram
        from app.models.care.risk_tier import DimRiskTier
        from app.models.care.need_type import NeedType
        
        self.programs = {p.program_name: p.id for p in db.query(DimProgram).all()}
        self.tiers = {t.tier_name: t.id for t in db.query(DimRiskTier).all()}
        self.dim_need_types = {t.need_name: t.id for t in db.query(NeedType).all()}

    def process_rules(self, db) -> List[EvaluationResult]:
        patient_view_rows = db.query(PatientDiagnosisView).all()
        # 2. Initialize Engine with desired strategies
        # TODO: These can be injected or managed via a factory
        engine = RulesEngine(strategies=[
            PrimaryCareWellnessStrategy(),
            DiabetesManagementStrategy()
        ])

        results = []

        for patient in patient_view_rows:
            result = engine.process_patient(patient)
            results.append(result)

        return results
    
    def prepare_evaluations_for_db(self, results: List[EvaluationResult]):
                
        eval_dicts = []
        for rule_results in results:
            for res in rule_results:
                # Look up the IDs based on names from the EvaluationResult
                program_id = self.programs.get(res.program_name)
                risk_tier_id = self.tiers.get(res.risk_tier) if res.risk_tier else None
                specialty_id = self.dim_need_types.get(res.specialty)
                
                if not program_id:
                    print(f"Warning: Program '{res.program_name}' not found in DB. Skipping.")
                    continue

                eval_dicts.append({
                    "patient_id": res.patient_id,
                    "program_id": program_id,
                    "eligible": res.eligible,
                    "risk_tier_id": risk_tier_id,
                    "specialty_id":  specialty_id,
                    "needs": res.needs,
                    "first_evaluated_at": res.evaluated_at,
                    "last_evaluated_at": res.evaluated_at,
                    "last_changed_at": res.evaluated_at,
                })
        
        return eval_dicts
    
    def bulk_upsert_evaluations(self, db, eval_dicts: List[Dict]):
        """
        eval_dicts: List of dictionaries with keys matching PatientEvaluation columns.
        Example: [{"patient_id": 1, "program_id": 10, ...}, {...}]
        """
        if not eval_dicts:
            return
        
        # 1. De-duplicate the list in Python first
        # We use (patient_id, program_id) as a unique key
        unique_evals = {}
        for entry in eval_dicts:
            key = (entry["patient_id"], entry["program_id"])
            # If there's a duplicate, the later one in the list wins
            unique_evals[key] = entry

        # Convert back to a list
        final_list = list(unique_evals.values())

        try:
            # 1. Prepare the bulk insert statement
            stmt = insert(PatientEvaluation).values(final_list)

            # 2. Define the 'Update' logic for rows that already exist
            upsert_stmt = stmt.on_conflict_do_update(
                # This MUST match the name of the UniqueConstraint in your model/DB
                constraint="uq_patient_evaluation_program",
                
                # 'stmt.excluded' refers to the data you just tried to insert
                set_={
                    "eligible": stmt.excluded.eligible,
                    "risk_tier_id": stmt.excluded.risk_tier_id,
                    "specialty_id": stmt.excluded.specialty_id,
                    "needs": stmt.excluded.needs,
                    "last_evaluated_at": stmt.excluded.last_evaluated_at,
                    "last_changed_at": stmt.excluded.last_changed_at,
                    "updated_at": func.now()  # Use DB server time for the audit stamp
                }
            )

            # 3. Execute once for the entire list
            db.execute(upsert_stmt)
            db.commit()
            print(f" Upsert records: {len(final_list):,}")
        except Exception as e:
            print("Error ", e)

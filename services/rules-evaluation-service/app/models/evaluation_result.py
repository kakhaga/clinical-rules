from typing import Dict, Any, Optional
from datetime import datetime

class EvaluationResult:
    patient_id: int
    program_name: str
    eligible: bool
    risk_tier: Optional[str] = None
    needs: Optional[str] = None
    specialty: Optional[str] = None
    evaluated_at: datetime = datetime.now()

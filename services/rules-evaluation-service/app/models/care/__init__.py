# Import the Base class
from app.db.base import Base

# Import ALL models here so Alembic can find them through Base.metadata
from app.models.care.risk_tier import DimRiskTier
from app.models.care.need_type import NeedType
from app.models.care.program import DimProgram
from app.models.care.patient_evaluation import PatientEvaluation

from sqlalchemy import Column, Integer, String, Date, BigInteger
from app.db.base import Base

class PatientEvaluationNeeds(Base):
    __tablename__ = "patient_evaluation_needs"
    __table_args__ = {"schema": "care"}

    # SQLAlchemy MUST have one primary_key=True to map the row.
    # We use the 'row_id' from the view's row_number column.
    row_id = Column(Integer, primary_key=True)
    patient_id = Column(BigInteger)    
    program_name = Column(String)
    tier_name = Column(String)
    previous_specialty_encounter = Column(String)
    specialty_need_name = Column(String)
    needs = Column(String)
    encounter_date = Column(Date)
    last_evaluated_at = Column(Date)
    days_since_last_evaluation = Column(Integer)
    cadence_days = Column(Integer)
    task_type = Column(String)

    # This makes the model read-only at the SQLAlchemy level
    __mapper_args__ = {
        "primary_key": [row_id],
        "always_refresh": True   # Ensures fresh data from the view
    }

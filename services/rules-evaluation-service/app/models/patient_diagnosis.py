from sqlalchemy import Column, Integer, String, Date, Float
from app.db.base_class import Base

class PatientDiagnosisView(Base):
    """
    Read-only model mapping to the care.patient_diagnoses view.
    """
    __tablename__ = "patient_diagnoses"
    __table_args__ = {"schema": "care"}

    # SQLAlchemy MUST have one primary_key=True to map the row.
    # We use the 'row_id' from the view's row_number column.
    row_id = Column(Integer, primary_key=True)
    id = Column(Integer)    
    date_of_birth = Column(Date)
    icd_code_ref = Column(String, nullable=True)
    icd_family = Column(String, nullable=True)
    test_name = Column(String)
    result_value = Column(Float)  # Adjust type if this is Text or Numeric
    diagnosed_date = Column(Date)

    # This makes the model read-only at the SQLAlchemy level
    __mapper_args__ = {
        "primary_key": [row_id],
        "always_refresh": True   # Ensures fresh data from the view
    }

    # Optional: Logic to prevent accidental writes at the ORM level
    def __repr__(self):
        return f"<PatientDiagnosis(id={self.id}, icd={self.icd_code_ref})>"
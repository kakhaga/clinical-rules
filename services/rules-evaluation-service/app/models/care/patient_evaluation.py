from sqlalchemy import (
    Column, 
    BigInteger, 
    Boolean, 
    DateTime, 
    ForeignKey,
    UniqueConstraint, 
    String,
    func,
    text 
)
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base

class PatientEvaluation(Base):
    __tablename__ = "patient_evaluation"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    patient_id = Column(BigInteger, nullable=False, index=True)
    eligible = Column(Boolean, nullable=False, index=True)
    
    # Ensure these point to the correct schema.table.column
    program_id = Column(BigInteger, nullable=True, index=True)
    risk_tier_id = Column(BigInteger, ForeignKey("care.dim_risk_tier.id"), nullable=True, index=True)
    
    # Cast the default to jsonb explicitly
    specialty_id = Column(BigInteger, nullable=True)
    needs = Column(String, nullable=True)
    
    first_evaluated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_evaluated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_changed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint('patient_id', 'program_id', name='uq_patient_evaluation_program'),
        {"schema": "care"}
    )

    def __repr__(self):
        # Using existing attributes
        return f"<PatientEvaluation(patient_id={self.patient_id}, program_id={self.program_id}, eligible={self.eligible})>"
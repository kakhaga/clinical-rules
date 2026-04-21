from sqlalchemy import Column, BigInteger, Text
from app.db.base import Base

class DimRiskTier(Base):
    __tablename__ = "dim_risk_tier"
    __table_args__ = {"schema": "care"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tier_name = Column(Text, nullable=False)
    tier_code = Column(Text, nullable=True)
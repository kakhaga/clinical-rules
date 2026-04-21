from sqlalchemy import Column, BigInteger, Text
from app.db.base import Base

class DimProgram(Base):
    __tablename__ = "dim_program"
    __table_args__ = {"schema": "care"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    program_name = Column(Text, nullable=False)
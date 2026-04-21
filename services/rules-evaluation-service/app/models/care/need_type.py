from sqlalchemy import Column, BigInteger, Text
from app.db.base import Base

class NeedType(Base):
    __tablename__ = "dim_need_types"
    __table_args__ = {"schema": "care"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    need_name = Column(Text, nullable=False)
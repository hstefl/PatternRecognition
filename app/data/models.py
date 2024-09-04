"""
Database tables definition.
"""

import enum

from .database import Base
from sqlalchemy import Column, Integer, String, Enum


class SeverityLevel(enum.Enum):
    low = "low"
    medium = "medium"
    critical = "critical"


class Recognition(Base):
    __tablename__ = 'recognitions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    severity = Column(Enum(SeverityLevel), nullable=False)
    location = Column(String, nullable=False)
    note = Column(String, nullable=True)

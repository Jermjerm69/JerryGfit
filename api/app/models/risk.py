from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


class RiskStatus(str, enum.Enum):
    OPEN = "open"
    MITIGATED = "mitigated"
    CLOSED = "closed"


class RiskSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskProbability(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RiskImpact(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Risk(Base):
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(Enum(RiskSeverity, values_callable=lambda x: [e.value for e in x]), default=RiskSeverity.MEDIUM)
    probability = Column(Enum(RiskProbability, values_callable=lambda x: [e.value for e in x]), default=RiskProbability.MEDIUM)
    impact = Column(Enum(RiskImpact, values_callable=lambda x: [e.value for e in x]), default=RiskImpact.MEDIUM)
    status = Column(Enum(RiskStatus, values_callable=lambda x: [e.value for e in x]), default=RiskStatus.OPEN)
    mitigation_plan = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="risks")

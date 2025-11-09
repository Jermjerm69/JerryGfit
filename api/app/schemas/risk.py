from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.risk import RiskStatus, RiskSeverity, RiskProbability, RiskImpact


class RiskBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: RiskSeverity = RiskSeverity.MEDIUM
    probability: RiskProbability = RiskProbability.MEDIUM
    impact: RiskImpact = RiskImpact.MEDIUM
    status: RiskStatus = RiskStatus.OPEN
    mitigation_plan: Optional[str] = None


class RiskCreate(RiskBase):
    pass


class RiskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[RiskSeverity] = None
    probability: Optional[RiskProbability] = None
    impact: Optional[RiskImpact] = None
    status: Optional[RiskStatus] = None
    mitigation_plan: Optional[str] = None


class RiskInDB(RiskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Risk(RiskInDB):
    pass

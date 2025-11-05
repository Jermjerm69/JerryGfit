from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "active"
    progress: float = 0.0
    due_date: Optional[datetime] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[float] = None
    due_date: Optional[datetime] = None


class Project(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

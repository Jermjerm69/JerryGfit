from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class EngagementMetric(Base):
    __tablename__ = "engagement_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    metric_type = Column(String, nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_metadata = Column(String, nullable=True)  # Renamed from 'metadata' (reserved word)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="engagement_metrics")

from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


class UserRole(str, enum.Enum):
    USER = "user"
    COACH = "coach"
    CREATOR = "creator"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable for OAuth users
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    google_id = Column(String, unique=True, nullable=True, index=True)  # Google OAuth ID
    role = Column(String, default="user", nullable=False, index=True)  # User role

    # Settings fields
    profile_picture = Column(String, nullable=True)  # Path or URL to profile picture
    notification_preferences = Column(JSON, nullable=True)  # Notification settings
    user_preferences = Column(JSON, nullable=True)  # Language, date format, etc.

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    risks = relationship("Risk", back_populates="owner", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
    ai_requests = relationship("AIRequest", back_populates="user", cascade="all, delete-orphan")
    engagement_metrics = relationship("EngagementMetric", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")

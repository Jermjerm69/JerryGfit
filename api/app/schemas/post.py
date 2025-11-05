from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    caption: Optional[str] = None
    hashtags: Optional[str] = None
    likes: int = 0
    comments: int = 0
    shares: int = 0
    engagement_rate: float = 0.0
    project_id: Optional[int] = None
    published_at: Optional[datetime] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    caption: Optional[str] = None
    hashtags: Optional[str] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    shares: Optional[int] = None
    engagement_rate: Optional[float] = None
    project_id: Optional[int] = None
    published_at: Optional[datetime] = None


class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

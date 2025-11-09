from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Dict, Any


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    profile_picture: Optional[str] = None
    notification_preferences: Optional[Dict[str, Any]] = None
    user_preferences: Optional[Dict[str, Any]] = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    profile_picture: Optional[str] = None
    notification_preferences: Optional[Dict[str, Any]] = None
    user_preferences: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDB):
    pass


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


class UserDataExport(BaseModel):
    user: Dict[str, Any]
    tasks: list
    risks: list
    projects: list
    posts: list
    ai_requests: list

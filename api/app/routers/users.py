from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
import uuid
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.task import Task
from app.models.risk import Risk
from app.models.project import Project
from app.models.post import Post
from app.models.ai_request import AIRequest
from app.schemas.user import User as UserSchema, UserUpdate, PasswordChange, UserDataExport
from app.core.security import get_current_user, get_password_hash, verify_password

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads/profile_pictures")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/me", response_model=UserSchema)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user


@router.put("/me", response_model=UserSchema)
def update_user_profile(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update user profile and preferences."""
    update_data = user_data.model_dump(exclude_unset=True)

    # Handle password update separately
    if "password" in update_data:
        current_user.hashed_password = get_password_hash(update_data.pop("password"))

    # Update other fields
    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/me/upload-photo")
async def upload_profile_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Upload profile picture."""
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only JPG, PNG, GIF, and WEBP are allowed."
        )

    # Validate file size (2MB max)
    file_size = 0
    chunk_size = 1024 * 1024  # 1MB
    temp_file = await file.read()
    file_size = len(temp_file)

    if file_size > 2 * 1024 * 1024:  # 2MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 2MB limit"
        )

    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(temp_file)

    # Delete old profile picture if exists
    if current_user.profile_picture:
        old_file = Path(current_user.profile_picture)
        if old_file.exists():
            old_file.unlink()

    # Update user
    current_user.profile_picture = str(file_path)
    db.commit()
    db.refresh(current_user)

    return {"message": "Profile picture uploaded successfully", "file_path": str(file_path)}


@router.post("/me/change-password")
def change_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Change user password."""
    # For OAuth users without password
    if not current_user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OAuth users cannot change password. Please set a password first."
        )

    # Verify current password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Validate new password length
    if len(password_data.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 8 characters long"
        )

    # Update password
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()

    return {"message": "Password changed successfully"}


@router.get("/me/export", response_model=UserDataExport)
def export_account_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Export all user account data."""
    # Get all user data
    tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()
    risks = db.query(Risk).filter(Risk.owner_id == current_user.id).all()
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    posts = db.query(Post).filter(Post.user_id == current_user.id).all()
    ai_requests = db.query(AIRequest).filter(AIRequest.user_id == current_user.id).all()

    # Prepare user data (exclude sensitive info)
    user_data = {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "profile_picture": current_user.profile_picture,
        "notification_preferences": current_user.notification_preferences,
        "user_preferences": current_user.user_preferences,
        "created_at": current_user.created_at.isoformat(),
        "updated_at": current_user.updated_at.isoformat(),
    }

    return {
        "user": user_data,
        "tasks": [task.__dict__ for task in tasks],
        "risks": [risk.__dict__ for risk in risks],
        "projects": [project.__dict__ for project in projects],
        "posts": [post.__dict__ for post in posts],
        "ai_requests": [req.__dict__ for req in ai_requests],
    }


@router.delete("/me")
def delete_account(
    password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete user account (requires password confirmation)."""
    # For OAuth users without password, allow deletion
    if current_user.hashed_password:
        # Verify password
        if not verify_password(password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password"
            )

    # Delete profile picture if exists
    if current_user.profile_picture:
        file_path = Path(current_user.profile_picture)
        if file_path.exists():
            file_path.unlink()

    # Delete user (cascade will delete all related data)
    db.delete(current_user)
    db.commit()

    return {"message": "Account deleted successfully"}

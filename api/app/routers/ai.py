from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from app.database import get_db
from app.models.user import User
from app.models.ai_request import AIRequest
from app.schemas.ai import AIGenerateRequest, AIGenerateResponse
from app.core.security import get_current_user

router = APIRouter()


@router.post("/generate", response_model=AIGenerateResponse)
def generate_ai_content(
    request: AIGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate AI content - returns mock data for now, OpenAI integration later."""

    # Mock data based on request type
    mock_data = []

    if request.request_type == "generate_risks":
        mock_data = [
            {
                "title": "Resource Allocation Risk",
                "description": "Insufficient team resources may delay project milestones",
                "severity": "high",
                "status": "open",
                "mitigation_plan": "Hire additional contractors or reallocate existing resources",
            },
            {
                "title": "Technology Stack Risk",
                "description": "New framework adoption may lead to learning curve delays",
                "severity": "medium",
                "status": "open",
                "mitigation_plan": "Provide comprehensive training and documentation",
            },
            {
                "title": "Market Competition Risk",
                "description": "Competitors launching similar features ahead of schedule",
                "severity": "high",
                "status": "open",
                "mitigation_plan": "Accelerate MVP development and early market entry",
            },
        ]
    elif request.request_type == "generate_tasks":
        mock_data = [
            {
                "title": "Set up development environment",
                "description": "Configure local dev environment with all dependencies",
                "status": "todo",
                "priority": "high",
                "due_date": (datetime.utcnow() + timedelta(days=2)).isoformat(),
            },
            {
                "title": "Design database schema",
                "description": "Create ERD and define all database tables",
                "status": "todo",
                "priority": "high",
                "due_date": (datetime.utcnow() + timedelta(days=3)).isoformat(),
            },
            {
                "title": "Implement authentication system",
                "description": "Build JWT-based auth with login/register endpoints",
                "status": "todo",
                "priority": "urgent",
                "due_date": (datetime.utcnow() + timedelta(days=5)).isoformat(),
            },
            {
                "title": "Create UI mockups",
                "description": "Design wireframes for all main application screens",
                "status": "todo",
                "priority": "medium",
                "due_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
            },
        ]
    else:  # generate_content
        mock_data = [
            {
                "type": "suggestion",
                "content": "Consider implementing feature flags for gradual rollout",
            },
            {
                "type": "suggestion",
                "content": "Add comprehensive error handling and logging",
            },
            {
                "type": "suggestion",
                "content": "Set up CI/CD pipeline for automated testing and deployment",
            },
        ]

    # Log AI request to database
    ai_request = AIRequest(
        user_id=current_user.id,
        request_type=request.request_type,
        prompt=request.prompt,
        response={"items": mock_data},
        tokens_used=random.randint(100, 500),  # Mock token count
    )
    db.add(ai_request)
    db.commit()

    return AIGenerateResponse(
        success=True,
        data=mock_data,
        tokens_used=ai_request.tokens_used,
        request_type=request.request_type,
    )

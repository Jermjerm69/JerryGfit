from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
import json
import logging

from app.database import get_db
from app.models.user import User
from app.models.ai_request import AIRequest
from app.schemas.ai import AIGenerateRequest, AIGenerateResponse
from app.core.security import get_current_user
from app.services.openai_service import openai_service

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/history")
def get_ai_history(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get AI generation history for the current user."""
    ai_requests = (
        db.query(AIRequest)
        .filter(AIRequest.user_id == current_user.id)
        .order_by(AIRequest.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return ai_requests


@router.post("/generate", response_model=AIGenerateResponse)
def generate_ai_content(
    request: AIGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate AI content using OpenAI API."""

    # Validate model parameter
    model = request.model or "gpt-4"
    if model not in ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]:
        model = "gpt-4"

    try:
        # Route to appropriate generation function based on request type
        if request.request_type == "caption":
            result = openai_service.generate_fitness_caption(
                context=request.prompt,
                tone="motivational",
                model=model
            )
            generated_data = [result]

        elif request.request_type == "hashtag":
            result = openai_service.generate_hashtags(
                caption=request.prompt,
                niche="fitness",
                count=15,
                model=model
            )
            generated_data = [result]

        elif request.request_type == "workout_plan":
            result = openai_service.generate_workout_plan(
                goal=request.prompt,
                level="intermediate",
                duration="30 minutes",
                model=model
            )
            generated_data = [result]

        elif request.request_type == "generate_risks":
            result = openai_service.generate_project_risks(
                project_description=request.prompt,
                model=model
            )
            # Parse JSON response if possible
            try:
                risks = json.loads(result["content"])
                generated_data = risks
                tokens_used = result["tokens_used"]
            except json.JSONDecodeError:
                # If not valid JSON, return as single item
                generated_data = [result]
                tokens_used = result["tokens_used"]

        elif request.request_type == "generate_tasks":
            result = openai_service.generate_task_breakdown(
                project_goal=request.prompt,
                timeframe="2 weeks",
                model=model
            )
            # Parse JSON response if possible
            try:
                tasks = json.loads(result["content"])
                generated_data = tasks
                tokens_used = result["tokens_used"]
            except json.JSONDecodeError:
                # If not valid JSON, return as single item
                generated_data = [result]
                tokens_used = result["tokens_used"]

        elif request.request_type == "content":
            result = openai_service.generate_general_content(
                request_type=request.request_type,
                prompt=request.prompt,
                model=model
            )
            generated_data = [result]

        else:
            # For any other request type, use general content generation
            result = openai_service.generate_general_content(
                request_type=request.request_type,
                prompt=request.prompt,
                model=model
            )
            generated_data = [result]

        # Extract tokens_used (handle both list and single result)
        if isinstance(generated_data, list) and len(generated_data) > 0:
            if isinstance(generated_data[0], dict) and "tokens_used" in generated_data[0]:
                tokens_used = generated_data[0]["tokens_used"]
            else:
                tokens_used = result.get("tokens_used", 0)
        else:
            tokens_used = result.get("tokens_used", 0)

        # Log AI request to database
        ai_request = AIRequest(
            user_id=current_user.id,
            request_type=request.request_type,
            prompt=request.prompt,
            response={"items": generated_data},
            tokens_used=tokens_used,
        )
        db.add(ai_request)
        db.commit()

        logger.info(f"AI generation successful for user {current_user.id}: {request.request_type}")

        return AIGenerateResponse(
            success=True,
            data=generated_data,
            tokens_used=tokens_used,
            request_type=request.request_type,
        )

    except ValueError as e:
        # OpenAI API key not configured
        logger.error(f"Configuration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )

    except Exception as e:
        # Handle all other errors
        logger.error(f"Error generating AI content: {e}")

        # Log failed request to database
        ai_request = AIRequest(
            user_id=current_user.id,
            request_type=request.request_type,
            prompt=request.prompt,
            response={"error": str(e)},
            tokens_used=0,
        )
        db.add(ai_request)
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate AI content: {str(e)}"
        )

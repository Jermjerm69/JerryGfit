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
    elif request.request_type == "caption":
        mock_data = [
            {
                "type": "fitness_caption",
                "content": "Transform your body, transform your life! 💪 Every workout is a step closer to your goals. Remember, the only bad workout is the one that didn't happen. Stay consistent, stay motivated, and watch the results follow! #FitnessJourney #NoPainNoGain",
            }
        ]
    elif request.request_type == "hashtag":
        mock_data = [
            {
                "type": "fitness_hashtags",
                "content": "#FitnessMotivation #GymLife #WorkoutRoutine #HealthyLifestyle #FitFam #TrainHard #FitnessGoals #BodyTransformation #GymMotivation #FitnessAddict #GetFit #FitnessInspiration #WorkoutMotivation #FitLife #GymTime",
            }
        ]
    elif request.request_type == "workout_plan":
        mock_data = [
            {
                "type": "workout_plan",
                "content": "**Upper Body Strength Workout**\n\nWarm-up (5 mins):\n- Arm circles: 30 seconds\n- Shoulder rolls: 30 seconds\n\nMain Workout:\n1. Push-ups: 3 sets x 12 reps\n2. Dumbbell Rows: 3 sets x 10 reps per arm\n3. Shoulder Press: 3 sets x 12 reps\n4. Bicep Curls: 3 sets x 15 reps\n5. Tricep Dips: 3 sets x 10 reps\n\nCool-down: 5 minutes stretching",
            }
        ]
    else:  # generate_content or other types
        mock_data = [
            {
                "type": "fitness_tip",
                "content": "💡 **Fitness Tip**: Consistency beats intensity. It's better to work out 3-4 times a week regularly than to go hard for a week and burn out. Build sustainable habits that you can maintain long-term for lasting results.",
            },
            {
                "type": "nutrition_tip",
                "content": "🥗 **Nutrition Tip**: Protein is essential for muscle recovery and growth. Aim for 1.6-2.2g per kg of body weight daily. Good sources include lean meats, fish, eggs, Greek yogurt, and plant-based options like lentils and tofu.",
            },
            {
                "type": "motivation",
                "content": "🔥 **Motivation**: Your body can stand almost anything. It's your mind you have to convince. When you feel like quitting, remember why you started. Every rep, every step, every healthy choice is an investment in yourself!",
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

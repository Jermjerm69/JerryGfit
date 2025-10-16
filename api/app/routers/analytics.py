from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.models.task import Task, TaskStatus
from app.models.risk import Risk, RiskStatus
from app.models.ai_request import AIRequest
from app.schemas.analytics import AnalyticsResponse, AnalyticsTotals, BurndownChart, BurndownDataPoint
from app.core.security import get_current_user

router = APIRouter()


@router.get("/", response_model=AnalyticsResponse)
def get_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get analytics data including totals and burndown chart."""

    # Calculate totals
    total_tasks = db.query(Task).filter(Task.owner_id == current_user.id).count()
    completed_tasks = (
        db.query(Task)
        .filter(Task.owner_id == current_user.id, Task.status == TaskStatus.DONE)
        .count()
    )

    total_risks = db.query(Risk).filter(Risk.owner_id == current_user.id).count()
    open_risks = (
        db.query(Risk)
        .filter(Risk.owner_id == current_user.id, Risk.status == RiskStatus.OPEN)
        .count()
    )

    ai_requests_count = (
        db.query(AIRequest).filter(AIRequest.user_id == current_user.id).count()
    )

    totals = AnalyticsTotals(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        total_risks=total_risks,
        open_risks=open_risks,
        ai_requests_count=ai_requests_count,
    )

    # Generate mock burndown chart data (last 14 days)
    burndown_data = []
    today = datetime.utcnow()

    for i in range(14, -1, -1):
        date = today - timedelta(days=i)
        # Mock calculation - in reality, you'd query historical data
        remaining = max(0, total_tasks - int((14 - i) * (completed_tasks / 14)) if total_tasks > 0 else 0)
        completed = total_tasks - remaining

        burndown_data.append(
            BurndownDataPoint(
                date=date,
                remaining_tasks=remaining,
                completed_tasks=completed,
            )
        )

    burndown = BurndownChart(data_points=burndown_data)

    return AnalyticsResponse(totals=totals, burndown=burndown)

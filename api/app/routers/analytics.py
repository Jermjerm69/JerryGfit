from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.models.task import Task, TaskStatus
from app.models.risk import Risk, RiskStatus, RiskProbability, RiskImpact
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

    # Calculate completion rate
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # Calculate velocity (tasks completed per week in the last 4 weeks)
    four_weeks_ago = datetime.utcnow() - timedelta(weeks=4)
    tasks_completed_last_4_weeks = (
        db.query(Task)
        .filter(
            Task.owner_id == current_user.id,
            Task.status == TaskStatus.DONE,
            Task.updated_at >= four_weeks_ago
        )
        .count()
    )
    velocity = tasks_completed_last_4_weeks / 4.0  # tasks per week

    # Calculate average lead time (average days to complete a task)
    completed_tasks_with_dates = (
        db.query(Task)
        .filter(
            Task.owner_id == current_user.id,
            Task.status == TaskStatus.DONE,
            Task.created_at.isnot(None),
            Task.updated_at.isnot(None)
        )
        .all()
    )

    if completed_tasks_with_dates:
        lead_times = [
            (task.updated_at - task.created_at).total_seconds() / 86400  # Convert to days
            for task in completed_tasks_with_dates
        ]
        average_lead_time = sum(lead_times) / len(lead_times)
    else:
        average_lead_time = 0

    # Calculate risk score (weighted average based on probability and impact)
    # Mapping: low=1, medium=2, high=3, critical=4
    probability_weight = {
        'low': 1,
        'medium': 2,
        'high': 3
    }
    impact_weight = {
        'low': 1,
        'medium': 2,
        'high': 3,
        'critical': 4
    }

    risks_with_scores = (
        db.query(Risk)
        .filter(
            Risk.owner_id == current_user.id,
            Risk.status == RiskStatus.OPEN
        )
        .all()
    )

    if risks_with_scores:
        risk_scores = [
            probability_weight.get(risk.probability.value, 2) * impact_weight.get(risk.impact.value, 2)
            for risk in risks_with_scores
        ]
        # Normalize to 0-100 scale (max possible score is 3*4=12)
        average_risk_score = (sum(risk_scores) / len(risk_scores)) / 12 * 100
    else:
        average_risk_score = 0

    totals = AnalyticsTotals(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        total_risks=total_risks,
        open_risks=open_risks,
        ai_requests_count=ai_requests_count,
        completion_rate=round(completion_rate, 2),
        velocity=round(velocity, 2),
        average_lead_time=round(average_lead_time, 2),
        risk_score=round(average_risk_score, 2),
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

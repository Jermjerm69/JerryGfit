from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime


class AnalyticsTotals(BaseModel):
    total_tasks: int
    completed_tasks: int
    total_risks: int
    open_risks: int
    ai_requests_count: int
    completion_rate: float  # Percentage of completed tasks
    velocity: float  # Tasks completed per week
    average_lead_time: float  # Average days to complete a task
    risk_score: float  # Calculated risk score (0-100)


class BurndownDataPoint(BaseModel):
    date: datetime
    remaining_tasks: int
    completed_tasks: int


class BurndownChart(BaseModel):
    data_points: List[BurndownDataPoint]


class RiskDistribution(BaseModel):
    low: int
    medium: int
    high: int
    critical: int


class VelocityDataPoint(BaseModel):
    week: str
    tasks_completed: int
    average: float


class AnalyticsResponse(BaseModel):
    totals: AnalyticsTotals
    burndown: BurndownChart
    risk_distribution: RiskDistribution
    velocity_data: List[VelocityDataPoint]

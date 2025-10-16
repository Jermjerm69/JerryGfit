from pydantic import BaseModel
from typing import List
from datetime import datetime


class AnalyticsTotals(BaseModel):
    total_tasks: int
    completed_tasks: int
    total_risks: int
    open_risks: int
    ai_requests_count: int


class BurndownDataPoint(BaseModel):
    date: datetime
    remaining_tasks: int
    completed_tasks: int


class BurndownChart(BaseModel):
    data_points: List[BurndownDataPoint]


class AnalyticsResponse(BaseModel):
    totals: AnalyticsTotals
    burndown: BurndownChart

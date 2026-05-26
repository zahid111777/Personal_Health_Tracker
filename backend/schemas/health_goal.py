from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class HealthGoalCreate(BaseModel):
    metric: str  # weight_kg|sleep_hours|steps|water_litres|mood_score|exercise_minutes
    goal_type: str  # reach|maintain|minimum|maximum
    target_value: float
    start_date: date
    target_date: Optional[date] = None


class HealthGoalUpdate(BaseModel):
    metric: Optional[str] = None
    goal_type: Optional[str] = None
    target_value: Optional[float] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    is_active: Optional[bool] = None


class HealthGoalResponse(BaseModel):
    id: int
    user_id: int
    metric: str
    goal_type: str
    target_value: float
    start_date: date
    target_date: Optional[date] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class GoalProgressResponse(BaseModel):
    goal: HealthGoalResponse
    current_value: Optional[float] = None
    progress_percentage: float
    days_remaining: Optional[int] = None
    on_track: bool

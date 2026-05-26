from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import Optional


class HealthLogCreate(BaseModel):
    log_date: date
    weight_kg: Optional[float] = None
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    heart_rate_bpm: Optional[int] = None
    sleep_hours: Optional[float] = None
    sleep_quality: Optional[int] = None
    mood_score: Optional[int] = None
    energy_level: Optional[int] = None
    water_litres: Optional[float] = None
    steps: Optional[int] = None
    calories_consumed: Optional[int] = None
    exercise_minutes: Optional[int] = None
    notes: Optional[str] = None

    @field_validator("systolic_bp", "diastolic_bp")
    @classmethod
    def validate_bp(cls, v, info):
        if v is not None and v < 0:
            raise ValueError("Blood pressure cannot be negative")
        return v

    @field_validator("sleep_quality")
    @classmethod
    def validate_sleep_quality(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError("Sleep quality must be between 1 and 5")
        return v

    @field_validator("mood_score", "energy_level")
    @classmethod
    def validate_score(cls, v):
        if v is not None and (v < 1 or v > 10):
            raise ValueError("Score must be between 1 and 10")
        return v


class HealthLogUpdate(HealthLogCreate):
    log_date: Optional[date] = None


class HealthLogResponse(BaseModel):
    id: int
    user_id: int
    log_date: date
    weight_kg: Optional[float] = None
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    heart_rate_bpm: Optional[int] = None
    sleep_hours: Optional[float] = None
    sleep_quality: Optional[int] = None
    mood_score: Optional[int] = None
    energy_level: Optional[int] = None
    water_litres: Optional[float] = None
    steps: Optional[int] = None
    calories_consumed: Optional[int] = None
    exercise_minutes: Optional[int] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

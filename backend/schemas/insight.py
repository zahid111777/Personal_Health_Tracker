from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class InsightResponse(BaseModel):
    id: int
    user_id: int
    insight_type: str
    metric_context: Optional[str] = None
    content: str
    data_summary_used: Optional[str] = None
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    created_at: datetime

    class Config:
        from_attributes = True


class QARequest(BaseModel):
    question: str


class QAResponse(BaseModel):
    question: str
    answer: str
    data_context: Optional[str] = None

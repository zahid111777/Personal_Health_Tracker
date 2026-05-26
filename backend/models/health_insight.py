from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class HealthInsight(Base):
    __tablename__ = "health_insights"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    insight_type = Column(String, nullable=False)  # weekly_summary|anomaly_explanation|correlation|recommendation|qa_response
    metric_context = Column(Text, nullable=True)  # JSON: which metrics
    content = Column(Text, nullable=False)  # LLM-generated text
    data_summary_used = Column(Text, nullable=True)  # JSON: pandas stats sent to LLM
    period_start = Column(Date, nullable=True)
    period_end = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="health_insights")

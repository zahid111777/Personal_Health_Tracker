from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class HealthGoal(Base):
    __tablename__ = "health_goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    metric = Column(String, nullable=False)  # weight_kg|sleep_hours|steps|water_litres|mood_score|exercise_minutes
    goal_type = Column(String, nullable=False)  # reach|maintain|minimum|maximum
    target_value = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    target_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="health_goals")

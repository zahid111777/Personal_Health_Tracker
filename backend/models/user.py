from sqlalchemy import Column, Integer, String, Boolean, Float, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")  # user | admin
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String, nullable=True)  # male | female | other
    height_cm = Column(Float, nullable=True)
    preferred_provider = Column(String, default="auto")  # auto|groq|openrouter|openai|gemini
    encrypted_groq_key = Column(String, nullable=True)
    encrypted_openrouter_key = Column(String, nullable=True)
    encrypted_openai_key = Column(String, nullable=True)
    encrypted_gemini_key = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    health_logs = relationship("HealthLog", back_populates="user", cascade="all, delete-orphan")
    health_goals = relationship("HealthGoal", back_populates="user", cascade="all, delete-orphan")
    health_insights = relationship("HealthInsight", back_populates="user", cascade="all, delete-orphan")

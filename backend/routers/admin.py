from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.user import User
from models.health_log import HealthLog
from models.health_insight import HealthInsight
from schemas.user import UserResponse
from services.auth_service import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
def get_platform_stats(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    total_users = db.query(func.count(User.id)).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    total_logs = db.query(func.count(HealthLog.id)).scalar()
    total_insights = db.query(func.count(HealthInsight.id)).scalar()
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_logs": total_logs,
        "total_insights": total_insights,
    }


@router.get("/users", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return db.query(User).all()


@router.put("/users/{user_id}/deactivate")
def deactivate_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate yourself")
    user.is_active = not user.is_active
    db.commit()
    return {"message": f"User {'deactivated' if not user.is_active else 'activated'}", "is_active": user.is_active}

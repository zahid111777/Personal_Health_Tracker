from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.health_goal import HealthGoal
from schemas.health_goal import HealthGoalCreate, HealthGoalUpdate, HealthGoalResponse, GoalProgressResponse
from services.auth_service import get_current_user
from services.goal_service import calculate_goal_progress, get_all_goals_progress

router = APIRouter(prefix="/goals", tags=["Health Goals"])

VALID_METRICS = {"weight_kg", "sleep_hours", "steps", "water_litres", "mood_score", "exercise_minutes"}
VALID_GOAL_TYPES = {"reach", "maintain", "minimum", "maximum"}


@router.post("", response_model=HealthGoalResponse, status_code=201)
def create_goal(data: HealthGoalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if data.metric not in VALID_METRICS:
        raise HTTPException(status_code=400, detail=f"Invalid metric. Valid: {VALID_METRICS}")
    if data.goal_type not in VALID_GOAL_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid goal type. Valid: {VALID_GOAL_TYPES}")

    goal = HealthGoal(user_id=current_user.id, **data.model_dump())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


@router.get("", response_model=list[HealthGoalResponse])
def list_goals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(HealthGoal).filter(
        HealthGoal.user_id == current_user.id, HealthGoal.is_active == True
    ).all()


@router.put("/{goal_id}", response_model=HealthGoalResponse)
def update_goal(goal_id: int, data: HealthGoalUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = db.query(HealthGoal).filter(HealthGoal.id == goal_id, HealthGoal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(goal, key, value)
    db.commit()
    db.refresh(goal)
    return goal


@router.delete("/{goal_id}", status_code=204)
def delete_goal(goal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = db.query(HealthGoal).filter(HealthGoal.id == goal_id, HealthGoal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal)
    db.commit()


@router.get("/progress", response_model=list[GoalProgressResponse])
def get_goals_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    results = get_all_goals_progress(db, current_user.id)
    return [
        GoalProgressResponse(
            goal=HealthGoalResponse.model_validate(r["goal"]),
            current_value=r["current_value"],
            progress_percentage=r["progress_percentage"],
            days_remaining=r["days_remaining"],
            on_track=r["on_track"],
        )
        for r in results
    ]

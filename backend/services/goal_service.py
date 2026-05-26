from datetime import date, timedelta
from sqlalchemy.orm import Session
from models.health_goal import HealthGoal
from services.analytics_service import get_metric_series


def calculate_goal_progress(db: Session, user_id: int, goal: HealthGoal) -> dict:
    df = get_metric_series(db, user_id, goal.metric, days=30)
    current_value = None
    progress = 0.0
    on_track = False

    if not df.empty:
        current_value = round(float(df["value"].iloc[-1]), 2)
        avg_recent = round(float(df["value"].tail(7).mean()), 2)

        if goal.goal_type == "reach":
            start_val = float(df["value"].iloc[0])
            total_range = goal.target_value - start_val
            if total_range != 0:
                progress = min(100, max(0, ((current_value - start_val) / total_range) * 100))
            on_track = progress >= 50 or (goal.target_date and (goal.target_date - date.today()).days > 7)
        elif goal.goal_type == "maintain":
            deviation = abs(current_value - goal.target_value)
            tolerance = goal.target_value * 0.1
            progress = max(0, min(100, (1 - deviation / tolerance) * 100)) if tolerance > 0 else 100
            on_track = deviation <= tolerance
        elif goal.goal_type == "minimum":
            progress = min(100, (avg_recent / goal.target_value) * 100) if goal.target_value > 0 else 100
            on_track = avg_recent >= goal.target_value
        elif goal.goal_type == "maximum":
            if avg_recent <= goal.target_value:
                progress = 100
                on_track = True
            else:
                progress = max(0, (goal.target_value / avg_recent) * 100) if avg_recent > 0 else 0

    days_remaining = None
    if goal.target_date:
        days_remaining = max(0, (goal.target_date - date.today()).days)

    return {
        "current_value": current_value,
        "progress_percentage": round(progress, 1),
        "days_remaining": days_remaining,
        "on_track": on_track,
    }


def get_all_goals_progress(db: Session, user_id: int) -> list:
    goals = db.query(HealthGoal).filter(
        HealthGoal.user_id == user_id,
        HealthGoal.is_active == True
    ).all()

    results = []
    for goal in goals:
        progress = calculate_goal_progress(db, user_id, goal)
        results.append({"goal": goal, **progress})
    return results

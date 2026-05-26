from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from database import get_db
from models.user import User
from services.auth_service import get_current_user
from services.analytics_service import (
    get_all_metrics_summary, get_metric_series, get_streak, get_log_frequency,
    calculate_moving_average
)
from services.anomaly_service import detect_anomalies
from services.correlation_service import calculate_correlation_matrix

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
def get_summary(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_metrics_summary(db, current_user.id, days)


@router.get("/metric/{metric}")
def get_metric_trend(metric: str, days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    df = get_metric_series(db, current_user.id, metric, days)
    if df.empty:
        return {"data": [], "moving_average": []}
    ma = calculate_moving_average(df["value"])
    return {
        "data": [{"date": str(row["date"]), "value": row["value"]} for _, row in df.iterrows()],
        "moving_average": [{"date": str(df.iloc[i]["date"]), "value": round(v, 2)} for i, v in enumerate(ma)],
    }


@router.get("/correlations")
def get_correlations(days: int = Query(60, ge=14, le=365), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return calculate_correlation_matrix(db, current_user.id, days)


@router.get("/anomalies")
def get_anomalies(days: int = Query(30, ge=7, le=365), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return detect_anomalies(db, current_user.id, days)


@router.get("/streak")
def get_current_streak(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"streak": get_streak(db, current_user.id)}


@router.get("/heatmap")
def get_heatmap(year: int = Query(default=None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if year is None:
        year = date.today().year
    return get_log_frequency(db, current_user.id, year)

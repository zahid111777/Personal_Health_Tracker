import pandas as pd
import numpy as np
from datetime import date, timedelta
from sqlalchemy.orm import Session
from models.health_log import HealthLog
from models.health_goal import HealthGoal

METRIC_COLUMNS = [
    "weight_kg", "systolic_bp", "diastolic_bp", "heart_rate_bpm",
    "sleep_hours", "sleep_quality", "mood_score", "energy_level",
    "water_litres", "steps", "calories_consumed", "exercise_minutes"
]

# Metrics where higher is better
HIGHER_IS_BETTER = {"sleep_hours", "sleep_quality", "mood_score", "energy_level", "water_litres", "steps", "exercise_minutes"}
# Metrics where lower is better
LOWER_IS_BETTER = {"weight_kg", "systolic_bp", "diastolic_bp"}


def get_metric_series(db: Session, user_id: int, metric: str, days: int = 30) -> pd.DataFrame:
    start_date = date.today() - timedelta(days=days)
    logs = (
        db.query(HealthLog)
        .filter(HealthLog.user_id == user_id, HealthLog.log_date >= start_date)
        .order_by(HealthLog.log_date)
        .all()
    )
    data = []
    for log in logs:
        val = getattr(log, metric, None)
        if val is not None:
            data.append({"date": log.log_date, "value": val})
    return pd.DataFrame(data)


def calculate_moving_average(series: pd.Series, window: int = 7) -> pd.Series:
    return series.rolling(window=window, min_periods=1).mean()


def calculate_trend(series: pd.Series) -> dict:
    if len(series) < 2:
        return {"slope": 0, "direction": "stable", "pct_change_7d": 0}
    x = np.arange(len(series))
    coefficients = np.polyfit(x, series.values, 1)
    slope = coefficients[0]
    threshold = 0.1 * abs(series.mean()) if series.mean() != 0 else 0.01
    if abs(slope) < threshold:
        direction = "stable"
    elif slope > 0:
        direction = "increasing"
    else:
        direction = "decreasing"

    pct_change = 0
    if len(series) >= 7:
        recent = series.iloc[-7:].mean()
        prior = series.iloc[:-7].mean() if len(series) > 7 else series.iloc[0]
        if prior != 0:
            pct_change = ((recent - prior) / abs(prior)) * 100

    return {"slope": round(float(slope), 4), "direction": direction, "pct_change_7d": round(pct_change, 2)}


def calculate_weekly_averages(db: Session, user_id: int, metric: str) -> pd.DataFrame:
    df = get_metric_series(db, user_id, metric, days=90)
    if df.empty:
        return pd.DataFrame()
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    weekly = df.resample("W").mean().reset_index()
    weekly.columns = ["week", "average"]
    return weekly


def get_all_metrics_summary(db: Session, user_id: int, days: int = 30) -> dict:
    summary = {}
    for metric in METRIC_COLUMNS:
        df = get_metric_series(db, user_id, metric, days)
        if df.empty or len(df) == 0:
            continue
        series = df["value"]
        trend = calculate_trend(series)
        summary[metric] = {
            "mean": round(float(series.mean()), 2),
            "median": round(float(series.median()), 2),
            "std": round(float(series.std()), 2) if len(series) > 1 else 0,
            "min": round(float(series.min()), 2),
            "max": round(float(series.max()), 2),
            "latest": round(float(series.iloc[-1]), 2),
            "trend_direction": trend["direction"],
            "trend_slope": trend["slope"],
            "pct_change_7d": trend["pct_change_7d"],
            "days_logged": len(series),
        }
    return summary


def get_streak(db: Session, user_id: int) -> int:
    logs = (
        db.query(HealthLog.log_date)
        .filter(HealthLog.user_id == user_id)
        .order_by(HealthLog.log_date.desc())
        .all()
    )
    if not logs:
        return 0
    dates = [log.log_date for log in logs]
    streak = 0
    expected = date.today()
    for d in dates:
        if d == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif d < expected:
            break
    return streak


def get_log_frequency(db: Session, user_id: int, year: int) -> dict:
    start = date(year, 1, 1)
    end = date(year, 12, 31)
    logs = (
        db.query(HealthLog.log_date)
        .filter(HealthLog.user_id == user_id, HealthLog.log_date >= start, HealthLog.log_date <= end)
        .all()
    )
    return {str(log.log_date): True for log in logs}

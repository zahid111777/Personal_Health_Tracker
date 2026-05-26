import pandas as pd
import numpy as np
from scipy import stats
from datetime import date, timedelta
from sqlalchemy.orm import Session
from models.health_log import HealthLog
from services.analytics_service import METRIC_COLUMNS


def interpret_correlation_strength(r: float) -> str:
    abs_r = abs(r)
    if abs_r < 0.3:
        return "weak"
    elif abs_r < 0.6:
        return "moderate"
    elif abs_r < 0.8:
        return "strong"
    return "very strong"


def calculate_correlation_matrix(db: Session, user_id: int, days: int = 60) -> dict:
    start_date = date.today() - timedelta(days=days)
    logs = (
        db.query(HealthLog)
        .filter(HealthLog.user_id == user_id, HealthLog.log_date >= start_date)
        .order_by(HealthLog.log_date)
        .all()
    )

    data = {}
    for metric in METRIC_COLUMNS:
        values = {}
        for log in logs:
            val = getattr(log, metric, None)
            if val is not None:
                values[log.log_date] = float(val)
        if len(values) >= 14:
            data[metric] = values

    if len(data) < 2:
        return {"matrix": {}, "significant_pairs": []}

    df = pd.DataFrame(data)
    df = df.dropna(how="all")

    matrix_raw = {}
    significant_pairs = []
    metrics = list(data.keys())

    for i, m1 in enumerate(metrics):
        matrix_raw[m1] = {}
        for j, m2 in enumerate(metrics):
            if i == j:
                matrix_raw[m1][m2] = 1.0
                continue
            paired = df[[m1, m2]].dropna()
            if len(paired) < 14:
                matrix_raw[m1][m2] = None
                continue
            corr, p_value = stats.pearsonr(paired[m1], paired[m2])
            matrix_raw[m1][m2] = round(float(corr), 3)

            if p_value < 0.05 and j > i:
                direction = "positive" if corr > 0 else "negative"
                significant_pairs.append({
                    "metric_a": m1,
                    "metric_b": m2,
                    "correlation": round(float(corr), 3),
                    "p_value": round(float(p_value), 4),
                    "direction": direction,
                    "strength": interpret_correlation_strength(corr),
                })

    significant_pairs.sort(key=lambda x: abs(x["correlation"]), reverse=True)

    return {"matrix": matrix_raw, "significant_pairs": significant_pairs}

import pandas as pd
import numpy as np
from scipy import stats
from datetime import date, timedelta
from sqlalchemy.orm import Session
from models.health_log import HealthLog
from services.analytics_service import METRIC_COLUMNS

# Metrics that tend to be skewed
SKEWED_METRICS = {"steps", "calories_consumed", "exercise_minutes"}


def detect_anomalies(db: Session, user_id: int, days: int = 30) -> list:
    start_date = date.today() - timedelta(days=days)
    logs = (
        db.query(HealthLog)
        .filter(HealthLog.user_id == user_id, HealthLog.log_date >= start_date)
        .order_by(HealthLog.log_date)
        .all()
    )
    if len(logs) < 7:
        return []

    anomalies = []
    for metric in METRIC_COLUMNS:
        values = []
        dates = []
        for log in logs:
            val = getattr(log, metric, None)
            if val is not None:
                values.append(float(val))
                dates.append(log.log_date)

        if len(values) < 7:
            continue

        series = pd.Series(values, index=dates)
        detected = _detect_metric_anomalies(series, metric)
        anomalies.extend(detected)

    return sorted(anomalies, key=lambda x: x["date"], reverse=True)


def _detect_metric_anomalies(series: pd.Series, metric: str) -> list:
    anomalies = []
    mean_val = series.mean()
    std_val = series.std()

    if std_val == 0:
        return []

    use_iqr = metric in SKEWED_METRICS
    if not use_iqr:
        try:
            _, p_value = stats.skewtest(series)
            use_iqr = p_value < 0.05
        except Exception:
            pass

    if use_iqr:
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        for d, val in series.items():
            if val < lower or val > upper:
                severity = "high" if (val < q1 - 3 * iqr or val > q3 + 3 * iqr) else "medium"
                anomalies.append({
                    "date": str(d),
                    "metric": metric,
                    "value": round(val, 2),
                    "expected_range": f"{round(lower, 2)} - {round(upper, 2)}",
                    "z_score": round((val - mean_val) / std_val, 2),
                    "severity": severity,
                    "method": "IQR",
                })
    else:
        z_scores = (series - mean_val) / std_val
        for d, (val, z) in zip(series.index, zip(series.values, z_scores.values)):
            if abs(z) > 2.5:
                severity = "high" if abs(z) > 3.5 else "medium"
                anomalies.append({
                    "date": str(d),
                    "metric": metric,
                    "value": round(val, 2),
                    "expected_range": f"{round(mean_val - 2 * std_val, 2)} - {round(mean_val + 2 * std_val, 2)}",
                    "z_score": round(float(z), 2),
                    "severity": severity,
                    "method": "Z-score",
                })

    return anomalies

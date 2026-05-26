from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.health_insight import HealthInsight
from schemas.insight import InsightResponse, QARequest, QAResponse
from services.auth_service import get_current_user
from services.insight_service import (
    generate_weekly_summary, explain_anomaly, explain_correlations, answer_health_qa
)
from services.anomaly_service import detect_anomalies

router = APIRouter(prefix="/insights", tags=["AI Insights"])


@router.post("/weekly", response_model=InsightResponse)
def create_weekly_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_profile = {
        "gender": current_user.gender,
        "height_cm": current_user.height_cm,
    }
    insight = generate_weekly_summary(db, current_user.id, user_profile)
    return insight


@router.post("/anomaly/{anomaly_index}")
def explain_anomaly_endpoint(anomaly_index: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    anomalies = detect_anomalies(db, current_user.id, days=30)
    if anomaly_index < 0 or anomaly_index >= len(anomalies):
        raise HTTPException(status_code=404, detail="Anomaly not found")
    explanation = explain_anomaly(db, current_user.id, anomalies[anomaly_index])
    return {"anomaly": anomalies[anomaly_index], "explanation": explanation}


@router.post("/correlations")
def explain_correlations_endpoint(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    explanation = explain_correlations(db, current_user.id)
    return {"explanation": explanation}


@router.post("/qa", response_model=QAResponse)
def qa_endpoint(data: QARequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    answer = answer_health_qa(db, current_user.id, data.question)
    return QAResponse(question=data.question, answer=answer)


@router.get("/history", response_model=list[InsightResponse])
def get_insight_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    insights = (
        db.query(HealthInsight)
        .filter(HealthInsight.user_id == current_user.id)
        .order_by(HealthInsight.created_at.desc())
        .limit(20)
        .all()
    )
    return insights

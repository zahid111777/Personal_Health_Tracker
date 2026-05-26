from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date
from typing import Optional
from database import get_db
from models.user import User
from models.health_log import HealthLog
from schemas.health_log import HealthLogCreate, HealthLogUpdate, HealthLogResponse
from services.auth_service import get_current_user

router = APIRouter(prefix="/logs", tags=["Health Logs"])


@router.post("", response_model=HealthLogResponse, status_code=201)
def create_log(data: HealthLogCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Validate BP
    if data.systolic_bp is not None and data.diastolic_bp is not None:
        if data.systolic_bp <= data.diastolic_bp:
            raise HTTPException(status_code=400, detail="Systolic must be greater than diastolic")

    log = HealthLog(user_id=current_user.id, **data.model_dump())
    try:
        db.add(log)
        db.commit()
        db.refresh(log)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="You already logged today. Edit existing log instead.")
    return log


@router.get("", response_model=list[HealthLogResponse])
def list_logs(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(HealthLog).filter(HealthLog.user_id == current_user.id)
    if start_date:
        query = query.filter(HealthLog.log_date >= start_date)
    if end_date:
        query = query.filter(HealthLog.log_date <= end_date)
    return query.order_by(HealthLog.log_date.desc()).offset(skip).limit(limit).all()


@router.get("/today", response_model=Optional[HealthLogResponse])
def get_today_log(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    log = db.query(HealthLog).filter(
        HealthLog.user_id == current_user.id, HealthLog.log_date == date.today()
    ).first()
    return log


@router.put("/{log_id}", response_model=HealthLogResponse)
def update_log(log_id: int, data: HealthLogUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    log = db.query(HealthLog).filter(HealthLog.id == log_id, HealthLog.user_id == current_user.id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    update_data = data.model_dump(exclude_unset=True)
    if "systolic_bp" in update_data and "diastolic_bp" in update_data:
        if update_data["systolic_bp"] is not None and update_data["diastolic_bp"] is not None:
            if update_data["systolic_bp"] <= update_data["diastolic_bp"]:
                raise HTTPException(status_code=400, detail="Systolic must be greater than diastolic")

    for key, value in update_data.items():
        setattr(log, key, value)
    db.commit()
    db.refresh(log)
    return log


@router.delete("/{log_id}", status_code=204)
def delete_log(log_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    log = db.query(HealthLog).filter(HealthLog.id == log_id, HealthLog.user_id == current_user.id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(log)
    db.commit()

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from services.auth_service import get_current_user
from services.report_service import generate_health_report

router = APIRouter(prefix="/export", tags=["Export"])


@router.get("/report")
def download_report(
    days: int = Query(30, ge=7, le=365),
    doctor_name: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pdf_bytes = generate_health_report(db, current_user.id, current_user.full_name, days, doctor_name)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=health_report_{current_user.full_name}.pdf"},
    )

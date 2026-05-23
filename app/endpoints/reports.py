from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import get_daily_summary

router = APIRouter()

@router.get("/reports/daily-summary")
def daily_summary(
    year: int = Query(..., description="Año (ej. 2026)"),
    month: int = Query(..., ge=1, le=12, description="Mes (1-12)"),
    db: Session = Depends(get_db)
):
    return get_daily_summary(db, year, month)
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.crud import get_mediciones_by_date_range, update_medicion
from app.schemas import MedicionResponse, MedicionUpdate

router = APIRouter()

@router.get("/measurements", response_model=list[MedicionResponse])
def get_measurements(
    start: datetime = Query(..., description="Fecha inicio (ISO 8601)"),
    end: datetime = Query(..., description="Fecha fin (ISO 8601)"),
    db: Session = Depends(get_db)
):
    if start > end:
        raise HTTPException(status_code=400, detail="start debe ser menor o igual que end")
    return get_mediciones_by_date_range(db, start, end)

@router.put("/measurements/{timestamp}", response_model=MedicionResponse)
def update_measurement(
    timestamp: datetime,
    data: MedicionUpdate,
    db: Session = Depends(get_db)
):
    updated = update_medicion(db, timestamp, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return updated
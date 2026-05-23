from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import get_last_medicion
from app.schemas import MedicionResponse

router = APIRouter()

@router.get("/latest", response_model=MedicionResponse)
def get_latest(db: Session = Depends(get_db)):
    medicion = get_last_medicion(db)
    if not medicion:
        raise HTTPException(status_code=404, detail="No hay registros en la base de datos")
    return medicion
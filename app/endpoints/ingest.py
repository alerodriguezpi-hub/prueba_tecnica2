from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import create_medicion
from app.schemas import MedicionCreate, MedicionResponse

router = APIRouter()

@router.post("/ingest", response_model=MedicionResponse, status_code=201)
def ingest_medicion(medicion: MedicionCreate, db: Session = Depends(get_db)):
    result = create_medicion(db, medicion)
    if result is None:
        raise HTTPException(status_code=409, detail="Ya existe un registro con ese timestamp")
    return result
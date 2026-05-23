from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime
from app import models, schemas

def get_last_medicion(db: Session):
    return db.query(models.Medicion).order_by(models.Medicion.timestamp.desc()).first()

def get_mediciones_by_date_range(db: Session, start: datetime, end: datetime):
    return db.query(models.Medicion).filter(
        and_(models.Medicion.timestamp >= start, models.Medicion.timestamp <= end)
    ).order_by(models.Medicion.timestamp.asc()).all()

def create_medicion(db: Session, medicion: schemas.MedicionCreate):
    existing = db.query(models.Medicion).filter(models.Medicion.timestamp == medicion.timestamp).first()
    if existing:
        return None
    
    estacion = db.query(models.Estacion).filter(models.Estacion.codigo == medicion.estacion_codigo).first()
    if not estacion:
        estacion = models.Estacion(codigo=medicion.estacion_codigo)
        db.add(estacion)
        db.commit()
        db.refresh(estacion)
    
    data_dict = medicion.dict(exclude={"estacion_codigo"}, exclude_unset=True)
    db_medicion = models.Medicion(estacion_id=estacion.id, **data_dict)
    
    db.add(db_medicion)
    db.commit()
    db.refresh(db_medicion)
    return db_medicion

def update_medicion(db: Session, timestamp: datetime, update_data: schemas.MedicionUpdate):
    db_medicion = db.query(models.Medicion).filter(models.Medicion.timestamp == timestamp).first()
    if not db_medicion:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(db_medicion, key, value)
    db.commit()
    db.refresh(db_medicion)
    return db_medicion

def get_daily_summary(db: Session, year: int, month: int):
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    results = db.query(
        func.date(models.Medicion.timestamp).label('dia'),
        func.sum(models.Medicion.precipitacion).label('precip_total'),
        func.max(models.Medicion.temperatura).label('temp_max'),
        func.min(models.Medicion.temperatura).label('temp_min')
    ).filter(
        and_(models.Medicion.timestamp >= start_date, models.Medicion.timestamp < end_date)
    ).group_by(func.date(models.Medicion.timestamp)).all()

    return [
        {
            "dia": r.dia,
            "precipitacion_total": r.precip_total or 0.0,
            "temperatura_maxima": r.temp_max,
            "temperatura_minima": r.temp_min
        }
        for r in results
    ]
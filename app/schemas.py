from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MedicionBase(BaseModel):
    timestamp: datetime
    estacion_codigo: Optional[int] = 193  # Asume 193 por defecto si el monitor no lo envía
    precipitacion: Optional[float] = 0.0
    temperatura: Optional[float] = 0.0
    humedad: Optional[float] = None
    velocidad_viento: Optional[float] = None
    direccion_viento: Optional[float] = None
    contador: Optional[int] = None
    numero1: Optional[float] = None
    numero2: Optional[float] = None
    numero3: Optional[float] = None
    jornada: Optional[str] = None

class MedicionCreate(MedicionBase):
    pass

class MedicionUpdate(BaseModel):
    precipitacion: Optional[float] = None
    temperatura: Optional[float] = None
    humedad: Optional[float] = None
    velocidad_viento: Optional[float] = None
    direccion_viento: Optional[float] = None
    contador: Optional[int] = None
    numero1: Optional[float] = None
    numero2: Optional[float] = None
    numero3: Optional[float] = None
    jornada: Optional[str] = None

class MedicionResponse(BaseModel):
    id: int
    timestamp: datetime
    precipitacion: float
    temperatura: float
    humedad: Optional[float]
    velocidad_viento: Optional[float]
    direccion_viento: Optional[float]

    class Config:
        orm_mode = True
        from_attributes = True
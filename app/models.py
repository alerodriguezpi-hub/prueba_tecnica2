from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Estacion(Base):
    __tablename__ = "estaciones"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(Integer, unique=True, nullable=False, index=True)
    
    mediciones = relationship("Medicion", back_populates="estacion")

class Medicion(Base):
    __tablename__ = "mediciones"

    id = Column(Integer, primary_key=True, index=True)
    estacion_id = Column(Integer, ForeignKey("estaciones.id"), nullable=False)
    timestamp = Column(DateTime, unique=True, nullable=False, index=True)  # fecha+hora unificada
    
    # Variables Meteorológicas
    precipitacion = Column(Float, default=0.0)
    temperatura = Column(Float, default=0.0)
    humedad = Column(Float, nullable=True)
    velocidad_viento = Column(Float, nullable=True)
    direccion_viento = Column(Float, nullable=True)
    
    # Campos adicionales (por si el monitor o archivos los envían)
    contador = Column(Integer, nullable=True)
    numero1 = Column(Float, nullable=True)
    numero2 = Column(Float, nullable=True)
    numero3 = Column(Float, nullable=True)
    jornada = Column(String, nullable=True)

    estacion = relationship("Estacion", back_populates="mediciones")
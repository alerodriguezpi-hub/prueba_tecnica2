from fastapi import FastAPI
from app.database import engine, Base
from app.endpoints import latest, measurements, ingest, reports

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Ambiental", version="1.0", description="API para datos meteorológicos e hidrológicos")

app.include_router(latest.router, prefix="/api", tags=["Último registro"])
app.include_router(measurements.router, prefix="/api", tags=["Históricos"])
app.include_router(ingest.router, prefix="/api", tags=["Ingesta"])
app.include_router(reports.router, prefix="/api", tags=["Reportes"])

@app.get("/")
def root():
    return {"mensaje": "API de datos ambientales - Prueba técnica"}
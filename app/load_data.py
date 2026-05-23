import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models

def cargar_datos():
    db = SessionLocal()
    
    # Cargar estaciones desde datos.csv
    df_datos = pd.read_csv("data/datos.csv")
    for cod in df_datos["estacion"].unique():
        existe = db.query(models.Estacion).filter(models.Estacion.codigo == cod).first()
        if not existe:
            db.add(models.Estacion(codigo=cod))
    db.commit()
    
    # Cargar mediciones
    for _, row in df_datos.iterrows():
        estacion = db.query(models.Estacion).filter(models.Estacion.codigo == row["estacion"]).first()
        if not estacion:
            continue
        timestamp_unix = row["fecha"] + row["tiempo"]
        dt = datetime.fromtimestamp(timestamp_unix)  # cambiamos utcfromtimestamp por fromtimestamp
        medicion = models.Medicion(
            estacion_id=estacion.id,
            timestamp=dt,
            precipitacion=row["lluvia"],
            temperatura=row["temperatura"],
            humedad=row["humedad"],
            velocidad_viento=row["velocidad_viento"],
            direccion_viento=row["direccion_viento"]
        )
        db.add(medicion)
    db.commit()
    db.close()
    print("Datos cargados exitosamente")

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    cargar_datos()

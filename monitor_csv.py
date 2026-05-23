import csv
import time
import os
import requests
from datetime import datetime

CSV_FECHA = os.path.join('data', 'fecha.csv')
CSV_TIEMPO = os.path.join('data', 'tiempo.csv')
API_INGEST_URL = 'http://localhost:8000/api/ingest'
INTERVALO_SEGUNDOS = 300
SOLO_CINCO_MINUTOS = True

def leer_fechas():
    fechas = []
    with open(CSV_FECHA, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            try:
                fecha = datetime.strptime(row['fecha'].strip(), '%d/%m/%Y').date()
                fechas.append(fecha)
            except Exception as e:
                print(f"Error fecha: {e} - fila: {row}")
                fechas.append(None)
    return fechas

def leer_tiempo_y_enviar(fechas):
    if not fechas:
        print("No hay fechas cargadas")
        return

    with open(CSV_TIEMPO, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        enviados = 0
        for idx, row in enumerate(reader):
            if idx >= len(fechas):
                print(f"Advertencia: tiempo.csv tiene más filas ({idx+1}) que fecha.csv ({len(fechas)}). Ignorando el resto.")
                break

            try:
                contador = int(row['contador'])
                if contador <= 0:
                    continue

                fecha = fechas[idx]
                if fecha is None:
                    continue

                hora_str = row['tiempo'].strip()
                if not hora_str:
                    continue

                hora = datetime.strptime(hora_str, '%H:%M:%S').time()

                if SOLO_CINCO_MINUTOS and (hora.minute % 5 != 0 or hora.second != 0):
                    continue

                timestamp = datetime.combine(fecha, hora)

                payload = {
                    "timestamp": timestamp.isoformat(),  # ejemplo: "2026-01-01T00:00:00"
                    "contador": contador,
                    "numero1": float(row['numero1']) if row['numero1'] else None,
                    "numero2": float(row['numero2']) if row['numero2'] else None,
                    "numero3": float(row['numero3']) if row['numero3'] else None,
                    "jornada": row['jornada'].strip() if row['jornada'] else None,
                    "precipitacion": 0.0,
                    "temperatura": 0.0
                }

                try:
                    r = requests.post(API_INGEST_URL, json=payload)
                    if r.status_code == 201:
                        print(f"[{datetime.now()}] Insertado: {timestamp}")
                        enviados += 1
                    elif r.status_code == 409:
                        print(f"[{datetime.now()}] Duplicado: {timestamp}")
                    else:
                        print(f"[{datetime.now()}] Error {r.status_code}: {r.text}")
                except Exception as e:
                    print(f"[{datetime.now()}] Error conexión: {e}")

                time.sleep(0.05)

            except Exception as e:
                print(f"Error procesando fila {idx+1}: {e} - Datos: {row}")

        print(f"[{datetime.now()}] Ciclo completado. Enviados nuevos: {enviados}")

def main():
    print("=== Monitor CSV unificado por orden de fila ===")
    print(f"Intervalo: {INTERVALO_SEGUNDOS}s, Filtrar cada 5 min: {SOLO_CINCO_MINUTOS}")
    fechas = leer_fechas()
    print(f"Se leyeron {len(fechas)} fechas")
    leer_tiempo_y_enviar(fechas)
    try:
        while True:
            time.sleep(INTERVALO_SEGUNDOS)
            leer_tiempo_y_enviar(fechas)
    except KeyboardInterrupt:
        print("\nMonitor detenido.")

if __name__ == "__main__":
    main()
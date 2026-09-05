"""
Run this after starting fresh (or any time you want to reset demo data):

    python scripts/seed_demo_data.py

It creates 3 demo AWS stations, generates 48 hours of realistic simulated sensor
readings (with injected spike/flatline/drift/missing faults) for each, trains an
Isolation Forest per station, and populates the database — so your dashboard has
real, explainable anomalies to show the moment you open it. No cloud, no manual
data entry needed.
"""
import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.database import SessionLocal, engine, Base
from app import models
from app.ml.simulator import generate_sensor_stream
from app.ml.detector import train_isolation_forest, detect_batch, classify_anomaly_type

STATIONS = [
    {"code": "AWS-001", "name": "Coimbatore AWS", "location": "Tamil Nadu"},
    {"code": "AWS-002", "name": "Chennai AWS", "location": "Tamil Nadu"},
    {"code": "AWS-003", "name": "Bengaluru AWS", "location": "Karnataka"},
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for s in STATIONS:
            station = db.query(models.Station).filter(models.Station.code == s["code"]).first()
            if not station:
                station = models.Station(**s)
                db.add(station)
                db.commit()
                db.refresh(station)

            df = generate_sensor_stream(station.code, hours=48, freq_minutes=5)
            model, baseline = train_isolation_forest(df, station.id)
            df = detect_batch(df, model)

            anomaly_count = 0
            for _, row in df.iterrows():
                wind = None if pd.isna(row["wind_speed"]) else float(row["wind_speed"])
                reading = models.SensorReading(
                    station_id=station.id,
                    timestamp=row["timestamp"],
                    temperature=float(row["temperature"]),
                    humidity=float(row["humidity"]),
                    pressure=float(row["pressure"]),
                    wind_speed=wind,
                    is_anomaly=bool(row["is_anomaly"]),
                    anomaly_score=float(row["anomaly_score"]),
                )
                db.add(reading)
                db.commit()
                db.refresh(reading)

                if row["is_anomaly"]:
                    reading_dict = {
                        "temperature": reading.temperature, "humidity": reading.humidity,
                        "pressure": reading.pressure, "wind_speed": reading.wind_speed,
                    }
                    anomaly_type = classify_anomaly_type(reading_dict, baseline)
                    anomaly = models.Anomaly(
                        reading_id=reading.id, station_id=station.id,
                        anomaly_type=anomaly_type, sensor="multi",
                        anomaly_score=reading.anomaly_score, value=reading.temperature,
                    )
                    db.add(anomaly)
                    db.commit()
                    anomaly_count += 1

            print(f"Seeded {len(df)} readings for {station.code} — {anomaly_count} anomalies flagged")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

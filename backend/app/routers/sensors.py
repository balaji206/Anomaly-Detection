from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app import models, schemas
from app.ml.detector import load_model, detect_single

router = APIRouter()


@router.get("/{station_id}/readings")
def get_readings(station_id: str, hours: int = 24, db: Session = Depends(get_db)):
    station = db.query(models.Station).filter(models.Station.code == station_id).first()
    if not station:
        raise HTTPException(404, f"Station '{station_id}' not found")

    since = datetime.utcnow() - timedelta(hours=hours)
    readings = (
        db.query(models.SensorReading)
        .filter(models.SensorReading.station_id == station.id, models.SensorReading.timestamp >= since)
        .order_by(models.SensorReading.timestamp)
        .all()
    )

    # Fallback: if no readings exist within the requested `hours` window, fetch the most recent readings
    if not readings:
        readings = (
            db.query(models.SensorReading)
            .filter(models.SensorReading.station_id == station.id)
            .order_by(models.SensorReading.timestamp.desc())
            .limit(hours * 12)
            .all()
        )
        readings = sorted(readings, key=lambda r: r.timestamp)

    return {
        "station_id": station.code,
        "readings": [
            {
                "timestamp": r.timestamp.isoformat(),
                "temperature": r.temperature,
                "humidity": r.humidity,
                "pressure": r.pressure,
                "wind_speed": r.wind_speed,
                "is_anomaly": r.is_anomaly,
            }
            for r in readings
        ],
    }


@router.post("/ingest")
def ingest_reading(reading: schemas.ReadingIn, db: Session = Depends(get_db)):
    station = db.query(models.Station).filter(models.Station.code == reading.station_code).first()
    if not station:
        station = models.Station(code=reading.station_code, name=reading.station_code, location="Unknown")
        db.add(station)
        db.commit()
        db.refresh(station)

    model, baseline = load_model(station.id)
    reading_dict = {
        "temperature": reading.temperature, "humidity": reading.humidity,
        "pressure": reading.pressure, "wind_speed": reading.wind_speed,
    }

    if model is None:
        # No trained model yet for this station (e.g. first-ever reading) — treat as normal,
        # run `python scripts/seed_demo_data.py` to get a trained baseline for realistic detection.
        is_anomaly, score, anomaly_type = False, 0.0, "normal"
    else:
        is_anomaly, score, anomaly_type = detect_single(model, baseline, reading_dict)

    db_reading = models.SensorReading(
        station_id=station.id, timestamp=reading.timestamp,
        temperature=reading.temperature, humidity=reading.humidity,
        pressure=reading.pressure, wind_speed=reading.wind_speed,
        is_anomaly=is_anomaly, anomaly_score=score,
    )
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)

    if is_anomaly:
        anomaly = models.Anomaly(
            reading_id=db_reading.id, station_id=station.id,
            anomaly_type=anomaly_type, sensor="multi",
            anomaly_score=score, value=reading.temperature,
        )
        db.add(anomaly)
        db.commit()

    return {"status": "ingested", "reading_id": db_reading.id, "is_anomaly": is_anomaly}

import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app import models
from app.ai.nvidia_client import explain_anomaly

router = APIRouter()


@router.get("")
def list_anomalies(station_id: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    query = db.query(models.Anomaly)
    if station_id:
        station = db.query(models.Station).filter(models.Station.code == station_id).first()
        if not station:
            return {"anomalies": []}
        query = query.filter(models.Anomaly.station_id == station.id)

    anomalies = query.order_by(models.Anomaly.detected_at.desc()).limit(limit).all()

    result = []
    for a in anomalies:
        station = db.get(models.Station, a.station_id)
        reading = db.get(models.SensorReading, a.reading_id) if a.reading_id else None
        result.append({
            "id": a.id,
            "station_id": station.code if station else None,
            "timestamp": reading.timestamp.isoformat() if reading else a.detected_at.isoformat(),
            "anomaly_type": a.anomaly_type,
            "anomaly_score": a.anomaly_score,
            "sensor": a.sensor,
            "value": a.value,
            "explanation": a.explanation,
            "resolved": a.resolved,
        })
    return {"anomalies": result}


@router.get("/{anomaly_id}/explain")
def get_explanation(anomaly_id: int, db: Session = Depends(get_db)):
    anomaly = db.get(models.Anomaly, anomaly_id)
    if not anomaly:
        raise HTTPException(404, "Anomaly not found")

    has_api_key = bool(os.getenv("NVIDIA_API_KEY"))
    is_valid_cached = (
        anomaly.explanation
        and not anomaly.explanation.startswith("Explanation temporarily unavailable")
        and not (has_api_key and anomaly.explanation.startswith("[Demo placeholder"))
    )

    if is_valid_cached:
        return {"explanation": anomaly.explanation}

    reading = db.get(models.SensorReading, anomaly.reading_id) if anomaly.reading_id else None
    reading_dict = {
        "temperature": reading.temperature if reading else None,
        "humidity": reading.humidity if reading else None,
        "pressure": reading.pressure if reading else None,
        "wind_speed": reading.wind_speed if reading else None,
    }

    explanation = explain_anomaly(reading_dict, anomaly.anomaly_score, anomaly.anomaly_type)
    if not explanation.startswith("Explanation temporarily unavailable"):
        anomaly.explanation = explanation
        db.commit()

    return {"explanation": explanation}

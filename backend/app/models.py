from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True)   # e.g. "AWS-001" — this is what the API/frontend use as station_id
    name = Column(String(100))
    location = Column(String(200))


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"))
    timestamp = Column(DateTime, nullable=False, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    wind_speed = Column(Float, nullable=True)
    is_anomaly = Column(Boolean, default=False)
    anomaly_score = Column(Float, nullable=True)


class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    reading_id = Column(Integer, ForeignKey("sensor_readings.id"))
    station_id = Column(Integer, ForeignKey("stations.id"))
    anomaly_type = Column(String(50))     # spike, flatline, drift, missing
    sensor = Column(String(50))
    anomaly_score = Column(Float)
    value = Column(Float, nullable=True)
    explanation = Column(String, nullable=True)   # filled in by NVIDIA NIM on first request, then cached
    detected_at = Column(DateTime, server_default=func.now())
    resolved = Column(Boolean, default=False)

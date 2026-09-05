from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import stations, sensors, anomalies

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AWS Anomaly Detection API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for local demo — tighten to your actual frontend URL before any real deployment
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stations.router, prefix="/api/stations", tags=["stations"])
app.include_router(sensors.router, prefix="/api/sensors", tags=["sensors"])
app.include_router(anomalies.router, prefix="/api/anomalies", tags=["anomalies"])


@app.get("/health")
def health():
    return {"status": "ok"}

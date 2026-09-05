from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReadingIn(BaseModel):
    """Body shape for POST /api/sensors/ingest — this is what the simulator/seed script sends."""
    station_code: str
    timestamp: datetime
    temperature: float
    humidity: float
    pressure: float
    wind_speed: Optional[float] = None

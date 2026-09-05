from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter()


@router.get("")
def list_stations(db: Session = Depends(get_db)):
    stations = db.query(models.Station).all()
    return {
        "stations": [
            {"id": s.code, "name": s.name, "location": s.location}
            for s in stations
        ]
    }

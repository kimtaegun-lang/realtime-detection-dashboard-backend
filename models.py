# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    zone = Column(String)
    uuid = Column(String)
    type = Column(String)  # Pedestrian / Bike / Vehicle / LargeVehicle
    x = Column(Float)
    y = Column(Float)
    speed_ms = Column(Float)
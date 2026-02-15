# schemas.py
from pydantic import BaseModel # python json 검증 라이브러리
from datetime import datetime
from typing import List # 리스트 타입 지정

class ObjectItem(BaseModel):
    uuid: str
    type: str
    x: float
    y: float
    speed_ms: float

class DetectionCreate(BaseModel):
    timestamp: datetime
    zone: str
    objects: List[ObjectItem]

class StatsResponse(BaseModel):
    total_count: int
    type_counts: dict
    avg_speed: float
    avg_speed_by_type: dict
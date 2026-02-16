# main.py 
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session # DB 세션 타입
from database import engine, get_db, SessionLocal
from models import Detection, Base # DB 테이블 클래스 및 Base
from schemas import DetectionCreate, StatsResponse,ObjectItem
from datetime import datetime, timedelta # timedelta는 시간 간격 계산에 사용
from typing import Optional # 값이 있을 수도 없을 수도 있는 파라미터에 사용
import asyncio # 비동기 처리 라이브러리
import json #  딕셔너리를 JSON 문자열로 변환
import random #  랜덤 값 생성. 더미 데이터 만들 때 써요
from uuid import uuid4 # 고유 ID 자동 생성
from httpx import AsyncClient # FastAPI 앱 내부에서 HTTP 요청 보내는 라이브러리.
from fastapi.middleware.cors import CORSMiddleware # CORS 설정을 위한 미들웨어

# DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 웹소켓 연결 관리
connected_clients = []


# 데이터 수신 POST /ingest
@app.post("/ingest")
async def ingest(data: DetectionCreate, db: Session = Depends(get_db)):
    for obj in data.objects:
        detection = Detection(
            timestamp=data.timestamp,
            zone=data.zone,
            uuid=obj.uuid,
            type=obj.type,
            x=obj.x,
            y=obj.y,
            speed_ms=obj.speed_ms
        )
        db.add(detection)
    db.commit()

    await broadcast(data) 
    return {"status": "ok"}

# 집계 API GET /stats
@app.get("/stats")
async def get_stats(
    from_dt: Optional[str] = Query(None, alias="from"),
    to_dt: Optional[str] = Query(None, alias="to"),
    zone: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Detection)

    if from_dt:
        query = query.filter(Detection.timestamp >= datetime.fromisoformat(from_dt))
    if to_dt:
        query = query.filter(Detection.timestamp <= datetime.fromisoformat(to_dt))
    if zone:
        query = query.filter(Detection.zone == zone)

    results = query.all()

    # 타입별 카운트
    type_counts = {"Pedestrian": 0, "Bike": 0, "Vehicle": 0, "LargeVehicle": 0}
    speed_by_type = {"Pedestrian": [], "Bike": [], "Vehicle": [], "LargeVehicle": []}

    for r in results:
        if r.type in type_counts:
            type_counts[r.type] += 1
            speed_by_type[r.type].append(r.speed_ms)

    avg_speed = round(sum(r.speed_ms for r in results) / len(results), 2) if results else 0
    avg_speed_by_type = {
        t: round(sum(v) / len(v), 2) if v else 0
        for t, v in speed_by_type.items()
    }

    return StatsResponse(
        total_count=len(results),
        type_counts=type_counts,
        avg_speed=avg_speed,
        avg_speed_by_type=avg_speed_by_type
    )

# 웹소켓 WS /ws
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

# 전체 클라이언트에 push
async def broadcast(data: DetectionCreate):
    payload = {
        "timestamp": data.timestamp.isoformat(),
        "zone": data.zone,
        "objects": [obj.dict() for obj in data.objects]
    }
    for client in connected_clients.copy():
        try:
            await client.send_text(json.dumps(payload))
        except:
            connected_clients.remove(client)

# 더미 데이터 자동 생성
@app.on_event("startup")
async def start_dummy_generator():
    asyncio.create_task(generate_dummy_data())

async def generate_dummy_data():
    while True:
        await asyncio.sleep(10)
        
        data = DetectionCreate(
            timestamp=datetime.utcnow(),
            zone=random.choice(["A구역", "B구역", "C구역"]),
            objects=[
                ObjectItem(
                    uuid=str(uuid4()),
                    type=random.choice(["Pedestrian", "Bike", "Vehicle", "LargeVehicle"]),
                    x=round(random.uniform(0, 100), 1),
                    y=round(random.uniform(0, 100), 1),
                    speed_ms=round(random.uniform(0.5, 30.0), 1)
                )
                for _ in range(random.randint(1, 5))
            ]
        )
        
        db = SessionLocal()
        try:
            await ingest(data, db)
        finally:
            db.close()
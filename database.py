# database.py
from sqlalchemy import create_engine # db엔진 연결 함수
from sqlalchemy.ext.declarative import declarative_base # 모델 클래스의 베이스 클래스
from sqlalchemy.orm import sessionmaker # 세션 생성기, 데이터베이스와의 대화에 사용
DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
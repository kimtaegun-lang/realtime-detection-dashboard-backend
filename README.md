# realtime-detection-dashboard-backend

1. 실행 방법 (백/프 각각 또는 docker-compose)

프론트
docker build -t frontend .
docker run -p 5173:5173 frontend


백엔드
docker build -t backend .
docker run -d -p 8000:8000 -e TZ=Asia/Seoul backend


2. API 사용 예시 (curl 또는 Postman 캡처)
   
<img width="1127" height="785" alt="stats_post" src="https://github.com/user-attachments/assets/1796246d-b3e1-4705-b890-0a836708d2f4" />
<img width="1121" height="633" alt="ingest_post" src="https://github.com/user-attachments/assets/0f15bb23-1f76-4455-9f72-03f9c424694d" />
<img width="1125" height="846" alt="websocket_post" src="https://github.com/user-attachments/assets/f8708fd4-9074-4531-ae4b-75a4599d2aa3" />


3. 간단 아키텍처 설명(텍스트/다이어그램)

<img width="696" height="538" alt="다이어그램" src="https://github.com/user-attachments/assets/c77f5ba5-57ea-40e3-a414-deae543fdc5b" />


<img width="1918" height="861" alt="대시보드" src="https://github.com/user-attachments/assets/d6d5a514-4bc4-4d5c-8610-5d59998c2158" />


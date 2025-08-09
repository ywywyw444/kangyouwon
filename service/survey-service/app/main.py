from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("survey_service")

# FastAPI 앱 생성
app = FastAPI(
    title="Survey Service",
    description="Survey service for ESG Mate",
    version="0.1.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 헬스 체크 엔드포인트
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "survey-service"}

# 루트 엔드포인트
@app.get("/")
async def root():
    return {"message": "Survey Service", "version": "0.1.0"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SERVICE_PORT", 8007))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv

# 환경 변수 로드
if os.getenv("RAILWAY_ENVIRONMENT") != "true":
    load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("auth_service")

# FastAPI 앱 생성
app = FastAPI(
    title="Auth Service",
    description="Authentication service for ESG Mate",
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

# auth_router import
from app.router.auth_router import auth_router

# 라우터 등록
app.include_router(auth_router)

# 헬스 체크 엔드포인트
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth-service"}

# 루트 엔드포인트
@app.get("/")
async def root():
    return {"message": "Auth Service", "version": "0.1.0"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SERVICE_PORT", 8008))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

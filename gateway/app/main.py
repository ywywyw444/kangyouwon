# app/main.py

import os
import sys
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from app.www.jwt_auth_middleware import AuthMiddleware
from app.common.utility.constant.settings import Settings
from app.router.main import router as gateway_router  # ✅ router로부터 가져옴

# 로컬 환경에서만 .env 로드
if os.getenv("RAILWAY_ENVIRONMENT") != "true":
    load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("gateway_api")

# 앱 생명주기 이벤트
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Gateway API 서비스 시작")
    app.state.settings = Settings()
    yield
    logger.info("🛑 Gateway API 서비스 종료")

# FastAPI 인스턴스 생성
app = FastAPI(
    title="Gateway API",
    description="Gateway API for http://ausikor.com",
    version="0.1.0",
    docs_url="/docs",
    lifespan=lifespan,
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://frontend:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 미들웨어 등록
app.add_middleware(AuthMiddleware)

# ✅ 라우터 등록 (router/main.py 내부에서 정의된 router)
app.include_router(gateway_router, prefix="/api/v1", tags=["Gateway API"])

# 기본 루트 경로
@app.get("/")
async def root():
    return {"message": "Gateway API", "version": "0.1.0"}

# 404 핸들러
from fastapi import Request
from fastapi.responses import JSONResponse
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "요청한 리소스를 찾을 수 없습니다."}
    )

# ✅ 앱 실행 (로컬 디버그용)
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SERVICE_PORT", 8080))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

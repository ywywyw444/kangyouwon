from typing import Optional, List
from fastapi import APIRouter, FastAPI, Request, UploadFile, File, Query, HTTPException, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging
import sys
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import Request

# from app.router.auth_router import auth_router
from app.www.jwt_auth_middleware import AuthMiddleware
from app.domain.discovery.model.service_discovery import ServiceDiscovery
from app.domain.discovery.model.service_type import ServiceType
from app.common.utility.constant.settings import Settings
from app.common.utility.factory.response_factory import ResponseFactory

if os.getenv("RAILWAY_ENVIRONMENT") != "true":
    load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("gateway_api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Gateway API 서비스 시작")
    # Settings 초기화 및 앱 state에 등록
    app.state.settings = Settings()
    yield
    logger.info("🛑 Gateway API 서비스 종료")

app = FastAPI(
title="Gateway API",
description="Gateway API for http://ausikor.com",
version="0.1.0",
docs_url="/docs",
lifespan=lifespan
)

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],  # 모든 origin 허용 (개발 환경용)
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)

gateway_router = APIRouter(prefix="/api/v1", tags=["Gateway API"])
# gateway_router.include_router(auth_router)
# 필요시: gateway_router.include_router(user_router)
app.include_router(gateway_router)

# 🪡🪡🪡 파일이 필요한 서비스 목록 (현재는 없음)
FILE_REQUIRED_SERVICES = set()

@app.get("/health", summary="테스트 엔드포인트")
async def health_check():
    return {"status": "healthy!"}

@app.post("/login", summary="로그인 엔드포인트")
async def login(request: Request):
    try:
        # 요청 본문을 JSON으로 파싱
        body = await request.json()
        username = body.get("username")
        password = body.get("password")
        
        # 간단한 검증
        if not username or not password:
            return JSONResponse(
                status_code=400,
                content={"error": "사용자명과 비밀번호를 입력해주세요."}
            )
        
        # 실제 로그인 로직은 여기에 구현
        # 현재는 테스트용으로 성공 응답만 반환
        
        # 로그인 성공 시 사용자 정보 출력
        logger.info(f"🔐 로그인 성공 - 사용자명: {username}, 비밀번호: {password}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "로그인 성공",
                "user": {
                    "username": username,
                    "id": "user_123"
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"로그인 처리 중 오류가 발생했습니다: {str(e)}"}
        )

@app.post("/signup", summary="회원가입 엔드포인트")
async def signup(request: Request):
    try:
        # 요청 본문을 JSON으로 파싱
        body = await request.json()
        industry = body.get("industry")
        email = body.get("email")
        name = body.get("name")
        age = body.get("age")
        auth_id = body.get("auth_id")
        auth_pw = body.get("auth_pw")
        
        # 필수 필드 검증
        if not industry or not auth_id or not auth_pw:
            return JSONResponse(
                status_code=400,
                content={"error": "업종, 아이디, 비밀번호는 필수 입력 항목입니다."}
            )
        
        # 실제 회원가입 로직은 여기에 구현
        # 현재는 테스트용으로 성공 응답만 반환
        
        # 회원가입 성공 시 사용자 정보 출력
        logger.info(f"📝 회원가입 성공 - 업종: {industry}, 이름: {name}, 아이디: {auth_id}")
        
        # 전체 JSON 데이터를 로그에 출력
        logger.info("=" * 50)
        logger.info("📋 회원가입 JSON 데이터:")
        logger.info(f"업종: {industry}")
        logger.info(f"이메일: {email}")
        logger.info(f"이름: {name}")
        logger.info(f"나이: {age}")
        logger.info(f"아이디: {auth_id}")
        logger.info(f"비밀번호: {auth_pw}")
        logger.info("=" * 50)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "회원가입 성공",
                "user": {
                    "industry": industry,
                    "email": email,
                    "name": name,
                    "age": age,
                    "auth_id": auth_id,
                    "id": "user_" + str(hash(auth_id))[-8:]  # 간단한 ID 생성
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"회원가입 처리 중 오류가 발생했습니다: {str(e)}"}
        )
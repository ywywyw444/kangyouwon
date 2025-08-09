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
from app.www.request_loggin import RequestLoggingMiddleware
from fastapi import APIRouter, Request, HTTPException, UploadFile, File, Query, Form, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from app.domain.discovery.model.service_discovery import ServiceDiscovery
from app.domain.discovery.model.service_type import ServiceType
from app.common.utility.factory.response_factory import ResponseFactory

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
        "http://frontend:3000",
        "https://kangyouwon.com",
        "https://www.kangyouwon.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 미들웨어 등록
app.add_middleware(AuthMiddleware)
app.add_middleware(RequestLoggingMiddleware, log_body=True)

# Gateway 라우터 정의
gateway_router = APIRouter(tags=["Gateway API"])

@gateway_router.post("/{service}/{path:path}")
async def proxy_post(...):
    logger.info("🔥🔥🔥🔥 POST 프록시 진입함!")
    ...

# 프록시 라우터 추가
@gateway_router.get("/{service}/{path:path}", summary="GET 프록시")
async def proxy_get(service: ServiceType, path: str, request: Request):
    try:
        factory = ServiceDiscovery(service_type=service)
        headers = dict(request.headers)
        
        response = await factory.request(
            method="GET",
            path=path,
            headers=headers
        )
        return ResponseFactory.create_response(response)
    except Exception as e:
        logger.error(f"Error in GET proxy: {str(e)}")
        return JSONResponse(
            content={"detail": f"Error processing request: {str(e)}"},
            status_code=500
        )

@gateway_router.post("/{service}/{path:path}", summary="POST 프록시")
async def proxy_post(
    service: ServiceType, 
    path: str,
    request: Request,
    file: Optional[UploadFile] = None,
    sheet_names: Optional[List[str]] = Query(None, alias="sheet_name")
):
    try:
        logger.info(f"🌈gateway.main.py🌈 POST 요청 받음: 서비스={service}, 경로={path}")
        logger.info(f"🔗 요청 URL: {request.url}")
        logger.info(f"📋 요청 헤더: {dict(request.headers)}")
        
        factory = ServiceDiscovery(service_type=service)
        
        # 헤더에서 Content-Length 제거 (httpx가 자동으로 계산)
        headers = dict(request.headers)
        headers.pop('content-length', None)
        
        # 요청 본문을 한 번만 읽기
        body = await request.body()
        data = None
        if body:
            try:
                import json
                data = json.loads(body)
                
                # 로그인/회원가입 데이터 구분하여 로깅
                if path == "login":
                    logger.info("🔐 === 로그인 요청 데이터 ===")
                    logger.info(f"👤 사용자명: {data.get('username', 'N/A')}")
                    logger.info(f"🔑 비밀번호: {'*' * len(data.get('password', '')) if data.get('password') else 'N/A'}")
                    logger.info(f"📦 전체 로그인 데이터: {json.dumps(data, ensure_ascii=False, indent=2)}")
                elif path == "signup":
                    logger.info("📝 === 회원가입 요청 데이터 ===")
                    logger.info(f"🏭 업종: {data.get('industry', 'N/A')}")
                    logger.info(f"📧 이메일: {data.get('email', 'N/A')}")
                    logger.info(f"👤 이름: {data.get('name', 'N/A')}")
                    logger.info(f"🎂 나이: {data.get('age', 'N/A')}")
                    logger.info(f"🆔 아이디: {data.get('auth_id', 'N/A')}")
                    logger.info(f"🔑 비밀번호: {'*' * len(data.get('auth_pw', '')) if data.get('auth_pw') else 'N/A'}")
                    logger.info(f"📦 전체 회원가입 데이터: {json.dumps(data, ensure_ascii=False, indent=2)}")
                else:
                    logger.info(f"📦 기타 POST 데이터: {json.dumps(data, ensure_ascii=False, indent=2)}")
                    
            except Exception as parse_error:
                logger.warning(f"⚠️ JSON 파싱 실패: {parse_error}")
                logger.warning(f"⚠️ 원본 데이터: {body}")
                pass
        
        logger.info(f"🚀 {service} 서비스로 요청 전송 중...")
        response = await factory.request(
            method="POST",
            path=path,
            headers=headers,
            data=data
        )
        
        logger.info(f"✅ {service} 서비스 응답 수신 완료")
        return ResponseFactory.create_response(response)
        
    except Exception as e:
        logger.error(f"❌ POST 요청 처리 중 오류 발생: {str(e)}")
        return JSONResponse(
            content={"detail": f"Gateway error: {str(e)}"},
            status_code=500
        )

# 헬스 체크 엔드포인트 (라우터에 추가)
@gateway_router.get("/health")
async def health_check():
    logger.info("🔍 Gateway 헬스 체크 요청")
    return {"status": "healthy", "service": "gateway", "version": "0.1.0"}

# 기본 루트 경로 (라우터에 추가)
@gateway_router.get("/")
async def root():
    logger.info(f"🌈gateway.main.py🌈")
    return {"message": "Gateway API", "version": "0.1.0"}

# ✅ 라우터 등록
app.include_router(gateway_router)

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
    logger.info(f"🌈gateway.main.py🌈")
    import uvicorn
    port = int(os.getenv("SERVICE_PORT", 8080))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

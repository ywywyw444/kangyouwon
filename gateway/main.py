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

from app.router.auth_router import auth_router
from http://app.www.google.jwt_auth_middleware import AuthMiddleware
from app.domain.discovery.model.service_discovery import ServiceDiscovery
from app.domain.discovery.model.service_type import ServiceType
from app.common.utility.constant.settings import Settings
from app.common.utility.factory.response_factory import ResponseFactory

if os.getenv("RAILWAY_ENVIRONMENT") != "true":
    load_dotenv()

logging.basicConfig(
    level=http://logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("gateway_api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    http://logger.info("🚀 Gateway API 서비스 시작")
    # Settings 초기화 및 앱 state에 등록
    app.state.settings = Settings()
    yield
    http://logger.info("🛑 Gateway API 서비스 종료")

app = FastAPI(
    title="Gateway API",
    description="Gateway API for http://ausikor.com",
    version="0.1.0",
    docs_url="/docs",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # 로컬 접근
        "http://127.0.0.1:3000",  # 로컬 IP 접근
        "http://frontend:3000",   # Docker 내부 네트워크

    ], # 프론트엔드 주소 명시
    allow_credentials=True,  # HttpOnly 쿠키 사용을 위해 필수
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)

gateway_router = APIRouter(prefix="/api/v1", tags=["Gateway API"])
gateway_router.include_router(auth_router)
# 필요시: gateway_router.include_router(user_router)
app.include_router(gateway_router)

# 🪡🪡🪡 파일이 필요한 서비스 목록 (현재는 없음)
FILE_REQUIRED_SERVICES = set()

@gateway_router.get("/health", summary="테스트 엔드포인트")
async def health_check():
    return {"status": "healthy!"}

@gateway_router.get("/{service}/{path:path}", summary="GET 프록시")
async def proxy_get(
    service: ServiceType, 
    path: str, 
    request: Request
):
    try:
        factory = ServiceDiscovery(service_type=service)
        
        # 헤더 전달 (JWT 및 사용자 ID - 미들웨어에서 이미 X-User-Id 헤더가 추가됨)
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

# 파일 업로드 및 일반 JSON 요청 모두 처리, JWT 적용
@gateway_router.post("/{service}/{path:path}", summary="POST 프록시")
async def proxy_post(
    service: ServiceType, 
    path: str,
    request: Request,
    file: Optional[UploadFile] = None,
    sheet_names: Optional[List[str]] = Query(None, alias="sheet_name")
):
    try:
        # 로깅
        http://logger.info(f"🌈 POST 요청 받음: 서비스={service}, 경로={path}")
        if file:
            http://logger.info(f"파일명: {file.filename}, 시트 이름: {sheet_names if sheet_names else '없음'}")

        # 서비스 팩토리 생성
        factory = ServiceDiscovery(service_type=service)
        
        # 요청 파라미터 초기화
        files = None
        params = None
        body = None
        data = None
        
        # 헤더 전달 (JWT 및 사용자 ID - 미들웨어에서 이미 X-User-Id 헤더가 추가됨)
        headers = dict(request.headers)
        
        # 파일이 필요한 서비스 처리
        if service in FILE_REQUIRED_SERVICES:
            # 파일이 필요한 서비스인 경우
            
            # 서비스 URI가 upload인 경우만 파일 체크
            if "upload" in path and not file:
                raise HTTPException(status_code=400, detail=f"서비스 {service}에는 파일 업로드가 필요합니다.")
            
            # 파일이 제공된 경우 처리
            if file:
                file_content = await http://file.read()
                files = {'file': (file.filename, file_content, file.content_type)}
                
                # 파일 위치 되돌리기 (다른 코드에서 다시 읽을 수 있도록)
                await http://file.seek(0)
            
            # 시트 이름이 제공된 경우 처리
            if sheet_names:
                params = {'sheet_name': sheet_names}
        else:
            # 일반 서비스 처리 (body JSON 전달)
            try:
                body = await request.body()
                if not body:
                    # body가 비어있는 경우도 허용
                    http://logger.info("요청 본문이 비어 있습니다.")
            except Exception as e:
                logger.warning(f"요청 본문 읽기 실패: {str(e)}")
                
        # 서비스에 요청 전달
        response = await factory.request(
            method="POST",
            path=path,
            headers=headers,
            body=body,
            files=files,
            params=params,
            data=data
        )
        
        # 응답 처리 및 반환
        return ResponseFactory.create_response(response)
        
    except HTTPException as he:
        # HTTP 예외는 그대로 반환
        return JSONResponse(
            content={"detail": he.detail},
            status_code=he.status_code
        )
    except Exception as e:
        # 일반 예외는 로깅 후 500 에러 반환
        logger.error(f"POST 요청 처리 중 오류 발생: {str(e)}")
        return JSONResponse(
            content={"detail": f"Gateway error: {str(e)}"},
            status_code=500
        )

# PUT - 일반 동적 라우팅 (JWT 적용)
@gateway_router.put("/{service}/{path:path}", summary="PUT 프록시")
async def proxy_put(service: ServiceType, path: str, request: Request):
    try:
        factory = ServiceDiscovery(service_type=service)
        
        # 헤더 전달 (JWT 및 사용자 ID - 미들웨어에서 이미 X-User-Id 헤더가 추가됨)
        headers = dict(request.headers)
        
        response = await factory.request(
            method="PUT",
            path=path,
            headers=headers,
            body=await request.body()
        )
        return ResponseFactory.create_response(response)
    except Exception as e:
        logger.error(f"Error in PUT proxy: {str(e)}")
        return JSONResponse(
            content={"detail": f"Error processing request: {str(e)}"},
            status_code=500
        )

# DELETE - 일반 동적 라우팅 (JWT 적용)
@gateway_router.delete("/{service}/{path:path}", summary="DELETE 프록시")
async def proxy_delete(service: ServiceType, path: str, request: Request):
    try:
        factory = ServiceDiscovery(service_type=service)
        
        # 헤더 전달 (JWT 및 사용자 ID - 미들웨어에서 이미 X-User-Id 헤더가 추가됨)
        headers = dict(request.headers)
        
        response = await factory.request(
            method="DELETE",
            path=path,
            headers=headers,
            body=await request.body()
        )
        return ResponseFactory.create_response(response)
    except Exception as e:
        logger.error(f"Error in DELETE proxy: {str(e)}")
        return JSONResponse(
            content={"detail": f"Error processing request: {str(e)}"},
            status_code=500
        )

# PATCH - 일반 동적 라우팅 (JWT 적용)
@gateway_router.patch("/{service}/{path:path}", summary="PATCH 프록시")
async def proxy_patch(service: ServiceType, path: str, request: Request):
    try:
        factory = ServiceDiscovery(service_type=service)
        
        # 헤더 전달 (JWT 및 사용자 ID - 미들웨어에서 이미 X-User-Id 헤더가 추가됨)
        headers = dict(request.headers)
        
        response = await factory.request(
            method="PATCH",
            path=path,
            headers=headers,
            body=await request.body()
        )
        return ResponseFactory.create_response(response)
    except Exception as e:
        logger.error(f"Error in PATCH proxy: {str(e)}")
        return JSONResponse(
            content={"detail": f"Error processing request: {str(e)}"},
            status_code=500
        )

# ✅ 메인 라우터 등록 (동적 라우팅)
# app.include_router(gateway_router) # 중복된 라우터 등록 제거

# 404 에러 핸들러
@app
.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "요청한 리소스를 찾을 수 없습니다."}
    )

# 기본 루트 경로
@app
.get("/")
async def root():
    return {"message": "Gateway API", "version": "0.1.0"}

# ✅ 서버 실행
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SERVICE_PORT", 8080))
    http://uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
import httpx
import asyncio
from typing import Dict, List, Optional
import logging
from datetime import datetime
import json
from pydantic import BaseModel
import os

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성 (Swagger UI 설정 포함)
app = FastAPI(
    title="MSA Gateway API",
    description="""
    ## MSA Gateway API Documentation
    
    이 API는 마이크로서비스 아키텍처의 Gateway 역할을 합니다.
    
    ### 주요 기능:
    - **Service Discovery**: 서비스 등록/해제 및 상태 관리
    - **Proxy Routing**: 모든 HTTP 메서드 지원 프록시 라우팅
    - **Health Check**: 서비스 헬스 체크 및 모니터링
    - **Load Balancing**: 기본적인 로드 밸런싱
    
    ### 사용 방법:
    1. Gateway 관리 API를 통해 서비스 상태 확인
    2. 프록시 라우팅을 통해 각 마이크로서비스에 접근
    3. 헬스 체크를 통한 서비스 모니터링
    
    ### 지원하는 서비스:
    - Account Service (`/account/*`)
    - Chatbot Service (`/chatbot/*`)
    - Company Service (`/company/*`)
    - Dashboard Service (`/dashboard/*`)
    - Facility Service (`/facility/*`)
    - KOSPI Service (`/kospi/*`)
    """,
    version="1.0.0",
    docs_url=None,  # 기본 docs 비활성화
    redoc_url=None,  # 기본 redoc 비활성화
    openapi_url="/openapi.json",
    contact={
        "name": "MSA Gateway Team",
        "email": "gateway@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {"url": "http://localhost:8000", "description": "Development server"},
        {"url": "https://gateway.example.com", "description": "Production server"},
    ],
    tags_metadata=[
        {
            "name": "Gateway Management",
            "description": "Gateway 상태 및 관리 API",
        },
        {
            "name": "Service Discovery",
            "description": "서비스 등록/해제 및 상태 관리",
        },
        {
            "name": "Health Check",
            "description": "서비스 헬스 체크 및 모니터링",
        },
        {
            "name": "Proxy Routing",
            "description": "마이크로서비스 프록시 라우팅",
        },
    ],
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서비스 레지스트리 (실제로는 Redis나 데이터베이스 사용)
SERVICE_REGISTRY = {
    "account-service": {
        "url": "http://localhost:8001",
        "health": "http://localhost:8001/health",
        "status": "healthy",
        "last_check": None
    },
    "chatbot-service": {
        "url": "http://localhost:8002",
        "health": "http://localhost:8002/health",
        "status": "healthy",
        "last_check": None
    },
    "company-service": {
        "url": "http://localhost:8003",
        "health": "http://localhost:8003/health",
        "status": "healthy",
        "last_check": None
    },
    "dashboard-service": {
        "url": "http://localhost:8004",
        "health": "http://localhost:8004/health",
        "status": "healthy",
        "last_check": None
    },
    "facility-service": {
        "url": "http://localhost:8005",
        "health": "http://localhost:8005/health",
        "status": "healthy",
        "last_check": None
    },
    "kospi-service": {
        "url": "http://localhost:8006",
        "health": "http://localhost:8006/health",
        "status": "healthy",
        "last_check": None
    }
}

# Pydantic 모델
class ServiceInfo(BaseModel):
    name: str
    url: str
    status: str
    last_check: Optional[datetime]

class HealthCheck(BaseModel):
    service: str
    status: str
    timestamp: datetime
    response_time: float

class ServiceRegistration(BaseModel):
    name: str
    url: str
    status: str = "healthy"
    last_check: Optional[datetime] = None

# 커스텀 Swagger UI 설정
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
        swagger_ui_parameters={
            "docExpansion": "list",
            "defaultModelsExpandDepth": 2,
            "defaultModelExpandDepth": 2,
            "showExtensions": True,
            "showCommonExtensions": True,
            "displayRequestDuration": True,
            "filter": True,
            "tryItOutEnabled": True,
        }
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.1.3/bundles/redoc.standalone.js",
    )

# 헬스 체크 함수
async def check_service_health(service_name: str, health_url: str) -> bool:
    """서비스 헬스 체크"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            start_time = datetime.now()
            response = await client.get(health_url)
            response_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                SERVICE_REGISTRY[service_name]["status"] = "healthy"
                SERVICE_REGISTRY[service_name]["last_check"] = datetime.now()
                logger.info(f"Service {service_name} is healthy (response time: {response_time:.3f}s)")
                return True
            else:
                SERVICE_REGISTRY[service_name]["status"] = "unhealthy"
                logger.warning(f"Service {service_name} is unhealthy (status: {response.status_code})")
                return False
    except Exception as e:
        SERVICE_REGISTRY[service_name]["status"] = "unhealthy"
        logger.error(f"Service {service_name} health check failed: {str(e)}")
        return False

# 서비스 디스커버리 함수
def discover_service(service_name: str) -> Optional[Dict]:
    """서비스 디스커버리"""
    if service_name in SERVICE_REGISTRY:
        service = SERVICE_REGISTRY[service_name]
        if service["status"] == "healthy":
            return service
    return None

# 프록시 라우팅 함수
async def proxy_request(service_name: str, path: str, method: str, request: Request) -> JSONResponse:
    """프록시 요청 처리"""
    service = discover_service(service_name)
    
    if not service:
        raise HTTPException(status_code=503, detail=f"Service {service_name} is not available")
    
    # 요청 데이터 추출
    body = None
    if method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.body()
        except:
            pass
    
    headers = dict(request.headers)
    # 호스트 헤더 제거 (타겟 서비스에서 설정)
    headers.pop("host", None)
    
    # 프록시 요청
    target_url = f"{service['url']}{path}"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if method == "GET":
                response = await client.get(target_url, headers=headers, params=request.query_params)
            elif method == "POST":
                response = await client.post(target_url, headers=headers, content=body)
            elif method == "PUT":
                response = await client.put(target_url, headers=headers, content=body)
            elif method == "DELETE":
                response = await client.delete(target_url, headers=headers)
            elif method == "PATCH":
                response = await client.patch(target_url, headers=headers, content=body)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")
            
            # 응답 헤더 설정
            response_headers = dict(response.headers)
            response_headers.pop("content-length", None)
            
            return JSONResponse(
                content=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                status_code=response.status_code,
                headers=response_headers
            )
    
    except httpx.RequestError as e:
        logger.error(f"Proxy request failed for {service_name}: {str(e)}")
        raise HTTPException(status_code=502, detail=f"Service {service_name} is not responding")
    except Exception as e:
        logger.error(f"Unexpected error in proxy request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# 라우트 정의

@app.get("/", tags=["Gateway Management"])
async def root():
    """
    Gateway 루트 엔드포인트
    
    Gateway의 기본 정보와 등록된 서비스 목록을 반환합니다.
    """
    return {
        "message": "MSA Gateway is running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "services": list(SERVICE_REGISTRY.keys()),
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Gateway Management"])
async def health_check():
    """
    Gateway 헬스 체크
    
    Gateway 서비스의 상태를 확인합니다.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "gateway": "MSA Gateway",
        "version": "1.0.0"
    }

@app.get("/services", tags=["Service Discovery"])
async def list_services():
    """
    등록된 서비스 목록 조회
    
    현재 Gateway에 등록된 모든 서비스의 정보를 반환합니다.
    """
    return {
        "services": [
            {
                "name": name,
                "url": service["url"],
                "status": service["status"],
                "last_check": service["last_check"].isoformat() if service["last_check"] else None
            }
            for name, service in SERVICE_REGISTRY.items()
        ]
    }

@app.post("/services/{service_name}/health", tags=["Health Check"])
async def check_service_health_endpoint(service_name: str):
    """
    특정 서비스 헬스 체크
    
    지정된 서비스의 헬스 상태를 확인합니다.
    """
    if service_name not in SERVICE_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
    
    service = SERVICE_REGISTRY[service_name]
    is_healthy = await check_service_health(service_name, service["health"])
    
    return {
        "service": service_name,
        "status": "healthy" if is_healthy else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "url": service["url"]
    }

@app.post("/services/health/all", tags=["Health Check"])
async def check_all_services_health():
    """
    모든 서비스 헬스 체크
    
    등록된 모든 서비스의 헬스 상태를 동시에 확인합니다.
    """
    tasks = []
    for service_name, service in SERVICE_REGISTRY.items():
        task = check_service_health(service_name, service["health"])
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    health_results = []
    for i, (service_name, result) in enumerate(zip(SERVICE_REGISTRY.keys(), results)):
        if isinstance(result, Exception):
            health_results.append({
                "service": service_name,
                "status": "error",
                "error": str(result),
                "timestamp": datetime.now().isoformat()
            })
        else:
            health_results.append({
                "service": service_name,
                "status": "healthy" if result else "unhealthy",
                "timestamp": datetime.now().isoformat()
            })
    
    return {"health_checks": health_results}

# 프록시 라우트들

@app.api_route("/account/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], tags=["Proxy Routing"])
async def proxy_account_service(path: str, request: Request):
    """
    Account Service 프록시
    
    Account Service로의 모든 요청을 프록시합니다.
    """
    return await proxy_request("account-service", f"/{path}", request.method, request)

@app.api_route("/chatbot/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], tags=["Proxy Routing"])
async def proxy_chatbot_service(path: str, request: Request):
    """
    Chatbot Service 프록시
    
    Chatbot Service로의 모든 요청을 프록시합니다.
    """
    return await proxy_request("chatbot-service", f"/{path}", request.method, request)

@app.api_route("/company/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], tags=["Proxy Routing"])
async def proxy_company_service(path: str, request: Request):
    """
    Company Service 프록시
    
    Company Service로의 모든 요청을 프록시합니다.
    """
    return await proxy_request("company-service", f"/{path}", request.method, request)

@app.api_route("/dashboard/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], tags=["Proxy Routing"])
async def proxy_dashboard_service(path: str, request: Request):
    """
    Dashboard Service 프록시
    
    Dashboard Service로의 모든 요청을 프록시합니다.
    """
    return await proxy_request("dashboard-service", f"/{path}", request.method, request)

@app.api_route("/facility/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], tags=["Proxy Routing"])
async def proxy_facility_service(path: str, request: Request):
    """
    Facility Service 프록시
    
    Facility Service로의 모든 요청을 프록시합니다.
    """
    return await proxy_request("facility-service", f"/{path}", request.method, request)

@app.api_route("/kospi/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], tags=["Proxy Routing"])
async def proxy_kospi_service(path: str, request: Request):
    """
    KOSPI Service 프록시
    
    KOSPI Service로의 모든 요청을 프록시합니다.
    """
    return await proxy_request("kospi-service", f"/{path}", request.method, request)

# 미들웨어: 요청 로깅
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """요청 로깅 미들웨어"""
    start_time = datetime.now()
    
    # 요청 로깅
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # 응답 로깅
    process_time = (datetime.now() - start_time).total_seconds()
    logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
    
    return response

# 서비스 등록/해제 엔드포인트
@app.post("/services/register", tags=["Service Discovery"])
async def register_service(service_info: ServiceRegistration):
    """
    새 서비스 등록
    
    새로운 서비스를 Gateway에 등록합니다.
    """
    SERVICE_REGISTRY[service_info.name] = {
        "url": service_info.url,
        "health": f"{service_info.url}/health",
        "status": service_info.status,
        "last_check": service_info.last_check
    }
    logger.info(f"Service registered: {service_info.name}")
    return {"message": f"Service {service_info.name} registered successfully"}

@app.delete("/services/{service_name}", tags=["Service Discovery"])
async def unregister_service(service_name: str):
    """
    서비스 등록 해제
    
    지정된 서비스를 Gateway에서 제거합니다.
    """
    if service_name in SERVICE_REGISTRY:
        del SERVICE_REGISTRY[service_name]
        logger.info(f"Service unregistered: {service_name}")
        return {"message": f"Service {service_name} unregistered successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Service {service_name} not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

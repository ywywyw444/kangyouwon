import httpx
import logging
from typing import Optional, Dict, Any
from .service_type import ServiceType

logger = logging.getLogger("gateway_api")

class ServiceDiscovery:
    def __init__(self, service_type: ServiceType):
        self.service_type = service_type
        
        # 환경에 따라 URL 설정
        import os
        is_local = os.getenv("ENVIRONMENT", "local") == "local"
        
        if is_local:
            # 로컬 개발 환경
            self.service_urls = {
                ServiceType.AUTH: "http://localhost:8001",
                ServiceType.CHATBOT: "http://localhost:8002",
                ServiceType.COMPANY: "http://localhost:8003",
                ServiceType.DASHBOARD: "http://localhost:8004",
                ServiceType.FACILITY: "http://localhost:8005",
                ServiceType.KOSPI: "http://localhost:8006",
            }
        else:
            # 배포 환경 - 실제 서비스 URL 사용
            self.service_urls = {
                ServiceType.AUTH: "https://auth-service.kangyouwon.com",
                ServiceType.CHATBOT: "https://chatbot-service.kangyouwon.com",
                ServiceType.COMPANY: "https://company-service.kangyouwon.com",
                ServiceType.DASHBOARD: "https://dashboard-service.kangyouwon.com",
                ServiceType.FACILITY: "https://facility-service.kangyouwon.com",
                ServiceType.KOSPI: "https://kospi-service.kangyouwon.com",
            }
    
    def get_service_url(self) -> str:
        """서비스 URL 반환"""
        return self.service_urls.get(self.service_type, "")
    
    async def request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        body: Optional[bytes] = None,
        files: Optional[Dict] = None,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> httpx.Response:
        """서비스에 요청 전달"""
        service_url = self.get_service_url()
        if not service_url:
            raise Exception(f"Unknown service type: {self.service_type}")
        
        # 전체 URL 구성
        full_url = f"{service_url}/{path}"
        
        logger.info(f"🔄 {method} 요청을 {self.service_type.value} 서비스로 전달: {full_url}")
        
        async with httpx.AsyncClient() as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(full_url, headers=headers, params=params)
                elif method.upper() == "POST":
                    response = await client.post(full_url, headers=headers, json=data, files=files, params=params)
                elif method.upper() == "PUT":
                    response = await client.put(full_url, headers=headers, json=data)
                elif method.upper() == "DELETE":
                    response = await client.delete(full_url, headers=headers)
                elif method.upper() == "PATCH":
                    response = await client.patch(full_url, headers=headers, json=data)
                else:
                    raise Exception(f"Unsupported HTTP method: {method}")
                
                logger.info(f"✅ {self.service_type.value} 서비스 응답: {response.status_code}")
                return response
                
            except httpx.RequestError as e:
                logger.error(f"❌ {self.service_type.value} 서비스 요청 실패: {str(e)}")
                raise Exception(f"Service request failed: {str(e)}")
            except Exception as e:
                logger.error(f"❌ {self.service_type.value} 서비스 오류: {str(e)}")
                raise

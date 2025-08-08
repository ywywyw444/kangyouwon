import httpx
import logging
from typing import Optional, Dict, Any
from .service_type import ServiceType

logger = logging.getLogger("gateway_api")

class ServiceDiscovery:
    def __init__(self, service_type: ServiceType):
        self.service_type = service_type
        self.service_urls = {
            ServiceType.AUTH: "http://auth-service:8001",
            ServiceType.CHATBOT: "http://chatbot-service:8002",
            ServiceType.COMPANY: "http://company-service:8003",
            ServiceType.DASHBOARD: "http://dashboard-service:8004",
            ServiceType.FACILITY: "http://facility-service:8005",
            ServiceType.KOSPI: "http://kospi-service:8006",
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

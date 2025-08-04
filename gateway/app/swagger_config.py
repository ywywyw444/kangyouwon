"""
Swagger UI 설정 파일
"""

# Swagger UI 커스텀 설정
SWAGGER_UI_CONFIG = {
    "docExpansion": "list",  # 모든 API 그룹을 펼침
    "defaultModelsExpandDepth": 2,  # 모델 확장 깊이
    "defaultModelExpandDepth": 2,  # 기본 모델 확장 깊이
    "showExtensions": True,  # 확장 정보 표시
    "showCommonExtensions": True,  # 공통 확장 정보 표시
    "displayRequestDuration": True,  # 요청 시간 표시
    "filter": True,  # 필터 기능 활성화
    "tryItOutEnabled": True,  # Try it out 기능 활성화
    "syntaxHighlight": {
        "activated": True,
        "theme": "monokai"
    },
    "persistAuthorization": True,  # 인증 정보 유지
    "displayOperationId": False,  # Operation ID 숨김
    "supportedSubmitMethods": ["get", "post", "put", "delete", "patch"],
}

# ReDoc 설정
REDOC_CONFIG = {
    "hideDownloadButton": False,
    "hideHostname": False,
    "hideLoading": False,
    "nativeScrollbars": False,
    "noAutoAuth": False,
    "pathInMiddlePanel": False,
    "requiredPropsFirst": True,
    "scrollYOffset": 0,
    "showExtensions": True,
    "sortPropsAlphabetically": True,
    "theme": {
        "colors": {
            "primary": {
                "main": "#1890ff"
            }
        },
        "typography": {
            "fontSize": "14px",
            "lineHeight": "1.5em",
            "code": {
                "fontSize": "13px",
                "fontFamily": "Courier, monospace",
                "color": "#e53935"
            },
            "headings": {
                "fontFamily": "Roboto, sans-serif",
                "fontWeight": "400"
            }
        }
    }
}

# API 태그 메타데이터
TAGS_METADATA = [
    {
        "name": "Gateway Management",
        "description": "Gateway 상태 및 관리 API",
        "externalDocs": {
            "description": "Gateway 관리 가이드",
            "url": "https://docs.example.com/gateway-management",
        },
    },
    {
        "name": "Service Discovery",
        "description": "서비스 등록/해제 및 상태 관리",
        "externalDocs": {
            "description": "서비스 디스커버리 가이드",
            "url": "https://docs.example.com/service-discovery",
        },
    },
    {
        "name": "Health Check",
        "description": "서비스 헬스 체크 및 모니터링",
        "externalDocs": {
            "description": "헬스 체크 가이드",
            "url": "https://docs.example.com/health-check",
        },
    },
    {
        "name": "Proxy Routing",
        "description": "마이크로서비스 프록시 라우팅",
        "externalDocs": {
            "description": "프록시 라우팅 가이드",
            "url": "https://docs.example.com/proxy-routing",
        },
    },
]

# 서버 정보
SERVERS = [
    {"url": "http://localhost:8000", "description": "Development server"},
    {"url": "https://gateway.example.com", "description": "Production server"},
    {"url": "https://staging-gateway.example.com", "description": "Staging server"},
]

# 연락처 정보
CONTACT_INFO = {
    "name": "MSA Gateway Team",
    "email": "gateway@example.com",
    "url": "https://github.com/example/msa-gateway",
}

# 라이선스 정보
LICENSE_INFO = {
    "name": "MIT",
    "url": "https://opensource.org/licenses/MIT",
} 
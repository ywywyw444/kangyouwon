# MSA Gateway

FastAPI 기반의 마이크로서비스 아키텍처 Gateway입니다. Proxy 패턴을 사용하여 서비스 디스커버리와 라우팅을 제공합니다.

## 🚀 주요 기능

- **Service Discovery**: 서비스 등록/해제 및 상태 관리
- **Proxy Routing**: 모든 HTTP 메서드 지원 프록시 라우팅
- **Health Check**: 서비스 헬스 체크 및 모니터링
- **Load Balancing**: 기본적인 로드 밸런싱 (향후 확장 예정)
- **Request Logging**: 모든 요청/응답 로깅
- **CORS Support**: 크로스 오리진 요청 지원
- **Swagger UI**: 완전한 API 문서화 및 테스트 인터페이스

## 📦 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
```bash
cp env.example .env
# .env 파일을 편집하여 실제 서비스 URL 설정
```

### 3. Gateway 실행
```bash
# 방법 1: Python 스크립트 사용
python run.py

# 방법 2: uvicorn 직접 실행
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## 📚 API 문서

Gateway는 완전한 API 문서화를 제공합니다:

- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`
- **OpenAPI JSON**: `http://localhost:8080/openapi.json`

### Swagger UI 특징
- ✅ 실시간 API 테스트
- ✅ 요청/응답 예시
- ✅ 스키마 검증
- ✅ 인증 지원
- ✅ 코드 생성
- ✅ 필터링 및 검색

## 🔧 API 엔드포인트

### Gateway 관리
- `GET /` - Gateway 상태 확인
- `GET /health` - Gateway 헬스 체크
- `GET /services` - 등록된 서비스 목록
- `POST /services/{service_name}/health` - 특정 서비스 헬스 체크
- `POST /services/health/all` - 모든 서비스 헬스 체크
- `POST /services/register` - 새 서비스 등록
- `DELETE /services/{service_name}` - 서비스 등록 해제

### 프록시 라우팅
- `GET/POST/PUT/DELETE/PATCH /account/{path}` - Account Service
- `GET/POST/PUT/DELETE/PATCH /chatbot/{path}` - Chatbot Service
- `GET/POST/PUT/DELETE/PATCH /company/{path}` - Company Service
- `GET/POST/PUT/DELETE/PATCH /dashboard/{path}` - Dashboard Service
- `GET/POST/PUT/DELETE/PATCH /facility/{path}` - Facility Service
- `GET/POST/PUT/DELETE/PATCH /kospi/{path}` - KOSPI Service

## 📊 서비스 레지스트리

현재 등록된 서비스들:

| 서비스명 | URL | 포트 | 상태 |
|---------|-----|------|------|
| account-service | http://localhost:8001 | 8001 | healthy |
| chatbot-service | http://localhost:8002 | 8002 | healthy |
| company-service | http://localhost:8003 | 8003 | healthy |
| dashboard-service | http://localhost:8004 | 8004 | healthy |
| facility-service | http://localhost:8005 | 8005 | healthy |
| kospi-service | http://localhost:8006 | 8006 | healthy |

## 🔍 사용 예시

### 1. 서비스 목록 조회
```bash
curl http://localhost:8080/services
```

### 2. 특정 서비스 헬스 체크
```bash
curl -X POST http://localhost:8080/services/auth-service/health
```

### 3. Account Service 프록시 요청
```bash
# 사용자 목록 조회
curl http://localhost:8080/auth/users

# 새 사용자 생성
curl -X POST http://localhost:8080/auth/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

### 4. 새 서비스 등록
```bash
curl -X POST http://localhost:8080/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "new-service",
    "url": "http://localhost:8007",
    "status": "healthy",
    "last_check": null
  }'
```

## 🏗️ 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client App    │    │   MSA Gateway   │    │  Microservices  │
│                 │    │                 │    │                 │
│  Frontend App   │───▶│  FastAPI App    │───▶│ Account Service │
│  Mobile App     │    │                 │    │ Chatbot Service │
│  API Client     │    │  Proxy Router   │    │ Company Service │
│  Swagger UI     │    │  Health Check   │    │ Dashboard Svc   │
└─────────────────┘    │  Service Disc   │    │ Facility Svc    │
                       │  API Docs       │    │ KOSPI Service   │
                       └─────────────────┘    └─────────────────┘
```

## 🔧 설정 옵션

### 환경 변수
- `GATEWAY_HOST`: Gateway 호스트 (기본값: 0.0.0.0)
- `GATEWAY_PORT`: Gateway 포트 (기본값: 8080)
- `GATEWAY_RELOAD`: 자동 리로드 (기본값: true)

### 서비스 URL 설정
각 서비스의 URL을 환경 변수로 설정할 수 있습니다:
- `ACCOUNT_SERVICE_URL`
- `CHATBOT_SERVICE_URL`
- `COMPANY_SERVICE_URL`
- `DASHBOARD_SERVICE_URL`
- `FACILITY_SERVICE_URL`
- `KOSPI_SERVICE_URL`

## 📈 모니터링

### 로그 확인
Gateway는 모든 요청과 응답을 로깅합니다:
```
INFO: Request: GET http://localhost:8080/account/users
INFO: Response: 200 - 0.123s
```

### 헬스 체크
```bash
# Gateway 헬스 체크
curl http://localhost:8080/health

# 모든 서비스 헬스 체크
curl -X POST http://localhost:8080/services/health/all
```

## 🚀 배포

### Docker 배포
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["python", "run.py"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  gateway:
    build: .
    ports:
      - "8080:8080"
    environment:
      - GATEWAY_HOST=0.0.0.0
      - GATEWAY_PORT=8080
```

## 🔒 보안

- CORS 설정으로 크로스 오리진 요청 제어
- 요청 헤더 검증
- 타임아웃 설정으로 DoS 공격 방지

## 📝 향후 개선 사항

- [ ] Redis를 사용한 서비스 레지스트리
- [ ] 로드 밸런싱 알고리즘 구현
- [ ] 인증/인가 미들웨어
- [ ] Rate Limiting
- [ ] Circuit Breaker 패턴
- [ ] 메트릭 수집 (Prometheus)
- [ ] 분산 추적 (Jaeger)

## 📄 라이선스

MIT License 
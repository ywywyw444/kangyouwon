# Materality - ChatGPT Clone

Next.js 기반의 PWA 웹 애플리케이션입니다.

## 기술 스택

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Styling**: Tailwind CSS
- **PWA**: Service Worker, Web App Manifest
- **Deployment**: Docker, Vercel, Railway
- **CI/CD**: GitHub Actions

## 주요 기능

- ✅ PWA (Progressive Web App) 지원
- ✅ 오프라인 기능
- ✅ 반응형 디자인
- ✅ 상태 관리 (Zustand)
- ✅ TypeScript 타입 안전성
- ✅ JSON 응답 처리
- ✅ 다중 플랫폼 배포 (Docker, Vercel, Railway)

## 개발 환경 설정

### 1. 의존성 설치

```bash
cd frontend
npm install
```

### 2. 환경 변수 설정

```bash
cp env.example .env.local
```

`.env.local` 파일을 편집하여 필요한 환경 변수를 설정하세요.

### 3. 개발 서버 실행

```bash
npm run dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000)을 열어 확인하세요.

## 배포 가이드

### 🐳 Docker 배포

#### 로컬 Docker 실행
```bash
# Docker 이미지 빌드
npm run docker:build

# Docker 컨테이너 실행
npm run docker:run

# Docker Compose 사용
npm run docker:compose
```

#### Docker Hub 배포
```bash
# 이미지 태그 설정
docker tag materality your-username/materality:latest

# Docker Hub에 푸시
docker push your-username/materality:latest
```

### ⚡ Vercel 배포

#### 1. Vercel CLI 설치
```bash
npm i -g vercel
```

#### 2. Vercel 로그인
```bash
vercel login
```

#### 3. 배포
```bash
npm run vercel:deploy
```

#### 4. GitHub Secrets 설정
- `VERCEL_TOKEN`: Vercel API 토큰
- `VERCEL_ORG_ID`: Vercel 조직 ID
- `VERCEL_PROJECT_ID`: Vercel 프로젝트 ID

### 🚂 Railway 배포

#### 1. Railway CLI 설치
```bash
npm i -g @railway/cli
```

#### 2. Railway 로그인
```bash
railway login
```

#### 3. 프로젝트 초기화
```bash
railway init
```

#### 4. 배포
```bash
npm run railway:deploy
```

#### 5. GitHub Secrets 설정
- `RAILWAY_TOKEN`: Railway API 토큰
- `RAILWAY_SERVICE`: Railway 서비스 이름

## CI/CD 파이프라인

GitHub Actions를 통해 자동화된 CI/CD 파이프라인이 구성되어 있습니다:

1. **Lint & Type Check**: ESLint와 TypeScript 타입 체크
2. **Build**: Next.js 애플리케이션 빌드
3. **Docker Build**: Docker 이미지 빌드
4. **Deploy**: main 브랜치에 푸시 시 자동 배포
   - Vercel 배포
   - Railway 배포

## 환경 변수

### 개발 환경
```env
NEXT_PUBLIC_API_URL=http://localhost:3000/api
NODE_ENV=development
```

### 프로덕션 환경
```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com/api
NODE_ENV=production
PORT=3000
```

## 프로젝트 구조

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── layout.tsx      # 루트 레이아웃
│   │   ├── page.tsx        # 메인 페이지
│   │   ├── globals.css     # 글로벌 스타일
│   │   └── api/            # API 라우트
│   │       └── health/     # 헬스체크 API
│   ├── components/          # React 컴포넌트
│   ├── store/              # Zustand 스토어
│   └── lib/                # 유틸리티
│       ├── api.ts          # Axios 설정
│       └── chatService.ts  # 채팅 서비스
├── public/                  # 정적 파일
├── Dockerfile              # Docker 설정
├── docker-compose.yml      # Docker Compose
├── railway.json           # Railway 설정
├── vercel.json            # Vercel 설정
└── package.json           # 의존성 관리
```

## 스크립트

### 개발
- `npm run dev`: 개발 서버 실행
- `npm run build`: 프로덕션 빌드
- `npm run start`: 프로덕션 서버 실행
- `npm run lint`: ESLint 실행
- `npm run type-check`: TypeScript 타입 체크

### Docker
- `npm run docker:build`: Docker 이미지 빌드
- `npm run docker:run`: Docker 컨테이너 실행
- `npm run docker:compose`: Docker Compose 실행
- `npm run docker:compose:down`: Docker Compose 중지

### 배포
- `npm run vercel:deploy`: Vercel 배포
- `npm run railway:deploy`: Railway 배포

## 헬스체크

모든 배포 플랫폼에서 헬스체크 엔드포인트를 제공합니다:

```
GET /api/health
```

응답 예시:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "uptime": 123.456,
  "environment": "production",
  "version": "1.0.0"
}
```

## 라이센스

MIT License 
# Materality - Multi-Platform Deployment

Next.js 기반의 ChatGPT 클론 애플리케이션으로, Docker, Vercel, Railway 모두에서 배포 가능합니다.

## 🚀 빠른 시작

### 로컬 개발
```bash
cd frontend
npm install
npm run dev
```

### Docker 배포
```bash
cd frontend
npm run docker:build
npm run docker:run
```

### Vercel 배포
```bash
cd frontend
npm run vercel:deploy
```

### Railway 배포
```bash
cd frontend
npm run railway:deploy
```

## 📁 프로젝트 구조

```
materality/
├── frontend/                 # Next.js 애플리케이션
│   ├── src/                 # 소스 코드
│   ├── public/              # 정적 파일
│   ├── Dockerfile           # Docker 설정
│   ├── docker-compose.yml   # Docker Compose
│   ├── railway.json         # Railway 설정
│   ├── vercel.json          # Vercel 설정
│   └── package.json         # 의존성 관리
├── .github/workflows/       # GitHub Actions CI/CD
└── README.md               # 프로젝트 문서
```

## 🛠️ 기술 스택

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios
- **PWA**: Service Worker, Web App Manifest
- **Deployment**: Docker, Vercel, Railway
- **CI/CD**: GitHub Actions

## 🚀 배포 플랫폼

### 🐳 Docker
- 멀티스테이지 빌드로 최적화된 이미지
- 헬스체크 지원
- Docker Compose로 로컬 개발 환경

### ⚡ Vercel
- 서버리스 함수 지원
- 자동 HTTPS
- 글로벌 CDN

### 🚂 Railway
- 컨테이너 기반 배포
- 자동 스케일링
- 실시간 로그

## 🔧 환경 설정

### GitHub Secrets 설정

#### Vercel 배포용
- `VERCEL_TOKEN`: Vercel API 토큰
- `VERCEL_ORG_ID`: Vercel 조직 ID
- `VERCEL_PROJECT_ID`: Vercel 프로젝트 ID

#### Railway 배포용
- `RAILWAY_TOKEN`: Railway API 토큰
- `RAILWAY_SERVICE`: Railway 서비스 이름

## 📋 주요 기능

- ✅ ChatGPT 스타일 인터페이스
- ✅ JSON 응답 처리
- ✅ PWA 지원
- ✅ 반응형 디자인
- ✅ 다중 플랫폼 배포
- ✅ 자동화된 CI/CD
- ✅ 헬스체크 엔드포인트

## 🔄 CI/CD 파이프라인

GitHub Actions를 통해 자동화된 배포 파이프라인:

1. **코드 품질 검사**: ESLint, TypeScript 체크
2. **빌드 테스트**: Next.js 빌드 검증
3. **Docker 빌드**: 컨테이너 이미지 생성
4. **자동 배포**: main 브랜치 푸시 시 자동 배포
   - Vercel 배포
   - Railway 배포

## 📖 상세 문서

각 플랫폼별 상세한 배포 가이드는 [frontend/README.md](frontend/README.md)를 참조하세요.

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🆘 지원

문제가 발생하거나 질문이 있으시면 [Issues](../../issues)를 통해 문의해 주세요. 
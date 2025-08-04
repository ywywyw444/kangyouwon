#!/bin/bash

# MSA Gateway Docker 실행 스크립트

echo "🚀 MSA Gateway Docker 실행 스크립트"
echo "=================================="

# 함수 정의
build_image() {
    echo "📦 Docker 이미지 빌드 중..."
    docker build -t msa-gateway .
    echo "✅ 이미지 빌드 완료"
}

run_container() {
    echo "🐳 컨테이너 실행 중..."
    docker run -d \
        --name msa-gateway \
        -p 8000:8000 \
        -e GATEWAY_HOST=0.0.0.0 \
        -e GATEWAY_PORT=8000 \
        -e GATEWAY_RELOAD=false \
        -e LOG_LEVEL=INFO \
        --restart unless-stopped \
        msa-gateway
    echo "✅ 컨테이너 실행 완료"
}

run_compose() {
    echo "🐳 Docker Compose로 전체 스택 실행 중..."
    docker-compose up -d
    echo "✅ 전체 스택 실행 완료"
}

stop_container() {
    echo "🛑 컨테이너 중지 중..."
    docker stop msa-gateway
    docker rm msa-gateway
    echo "✅ 컨테이너 중지 완료"
}

stop_compose() {
    echo "🛑 Docker Compose 스택 중지 중..."
    docker-compose down
    echo "✅ 스택 중지 완료"
}

show_logs() {
    echo "📋 로그 확인 중..."
    docker logs msa-gateway
}

show_status() {
    echo "📊 컨테이너 상태 확인 중..."
    docker ps -a | grep msa-gateway
}

# 메인 로직
case "$1" in
    "build")
        build_image
        ;;
    "run")
        build_image
        run_container
        ;;
    "compose")
        run_compose
        ;;
    "stop")
        stop_container
        ;;
    "stop-compose")
        stop_compose
        ;;
    "logs")
        show_logs
        ;;
    "status")
        show_status
        ;;
    "restart")
        stop_container
        run_container
        ;;
    *)
        echo "사용법: $0 {build|run|compose|stop|stop-compose|logs|status|restart}"
        echo ""
        echo "명령어 설명:"
        echo "  build        - Docker 이미지만 빌드"
        echo "  run          - 단일 컨테이너로 실행"
        echo "  compose      - Docker Compose로 전체 스택 실행"
        echo "  stop         - 단일 컨테이너 중지"
        echo "  stop-compose - Docker Compose 스택 중지"
        echo "  logs         - 로그 확인"
        echo "  status       - 컨테이너 상태 확인"
        echo "  restart      - 컨테이너 재시작"
        echo ""
        echo "예시:"
        echo "  $0 run       # 단일 컨테이너 실행"
        echo "  $0 compose   # 전체 스택 실행"
        echo "  $0 logs      # 로그 확인"
        exit 1
        ;;
esac

echo ""
echo "🌐 Gateway 접속 정보:"
echo "  - URL: http://localhost:8000"
echo "  - Health Check: http://localhost:8000/health"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Services: http://localhost:8000/services" 
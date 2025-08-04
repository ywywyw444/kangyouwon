#!/usr/bin/env python3
"""
MSA Gateway 실행 스크립트
"""

import uvicorn
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

if __name__ == "__main__":
    # 서버 설정
    host = os.getenv("GATEWAY_HOST", "0.0.0.0")
    port = int(os.getenv("GATEWAY_PORT", "8000"))
    reload = os.getenv("GATEWAY_RELOAD", "true").lower() == "true"
    
    print(f"🚀 Starting MSA Gateway on {host}:{port}")
    print(f"📊 Health Check: http://{host}:{port}/health")
    print(f"📋 Services: http://{host}:{port}/services")
    print(f"📚 API Docs: http://{host}:{port}/docs")
    
    # 서버 실행
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    ) 
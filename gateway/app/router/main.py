# app/router/auth.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import logging

router = APIRouter()
logger = logging.getLogger("gateway_api")

@router.post("/login", summary="로그인 엔드포인트")
async def login(request: Request):
    logger.info("❤️❤️❤️❤️❤️login")
    try:
        body = await request.json()
        username = body.get("username")
        password = body.get("password")

        if not username or not password:
            return JSONResponse(
                status_code=400,
                content={"error": "사용자명과 비밀번호를 입력해주세요."}
            )

        logger.info(f"🔐 로그인 성공 - 사용자명: {username}, 비밀번호: {password}")

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "로그인 성공",
                "user": {
                    "username": username,
                    "id": "user_123"
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"로그인 처리 중 오류가 발생했습니다: {str(e)}"}
        )

@router.post("/signup", summary="회원가입 엔드포인트")
async def signup(request: Request):
    logger.info("💚💚💚💚💚signup")
    try:
        body = await request.json()
        industry = body.get("industry")
        email = body.get("email")
        name = body.get("name")
        age = body.get("age")
        auth_id = body.get("auth_id")
        auth_pw = body.get("auth_pw")

        if not industry or not auth_id or not auth_pw:
            return JSONResponse(
                status_code=400,
                content={"error": "업종, 아이디, 비밀번호는 필수 입력 항목입니다."}
            )

        logger.info(f"📝 회원가입 성공 - 업종: {industry}, 이름: {name}, 아이디: {auth_id}")
        logger.info("=" * 50)
        logger.info("📋 회원가입 JSON 데이터:")
        logger.info(f"업종: {industry}")
        logger.info(f"이메일: {email}")
        logger.info(f"이름: {name}")
        logger.info(f"나이: {age}")
        logger.info(f"아이디: {auth_id}")
        logger.info(f"비밀번호: {auth_pw}")
        logger.info("=" * 50)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "회원가입 성공",
                "user": {
                    "industry": industry,
                    "email": email,
                    "name": name,
                    "age": age,
                    "auth_id": auth_id,
                    "id": "user_" + str(hash(auth_id))[-8:]
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"회원가입 처리 중 오류가 발생했습니다: {str(e)}"}
        )

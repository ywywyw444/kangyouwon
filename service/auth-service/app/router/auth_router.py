from fastapi import APIRouter, Cookie, HTTPException, Query
from fastapi.responses import JSONResponse
from app.domain.controller.auth_controller import AuthController, LoginRequest, SignupRequest

# Google OAuth는 나중에 구현
# from app.domain.auth.controller.google_controller import GoogleController

auth_router = APIRouter(prefix="/auth", tags=["auth"])
# google_controller = GoogleController()
auth_controller = AuthController()

@auth_router.post("/login", summary="사용자 로그인")
async def login(login_data: LoginRequest):
    """
    사용자명과 비밀번호로 로그인을 처리합니다.
    """
    import logging
    import json
    logger = logging.getLogger("auth_service")
    
    logger.info("🔐 === Auth Service 로그인 요청 ===")
    logger.info(f"👤 사용자명: {login_data.username}")
    logger.info(f"🔑 비밀번호: {'*' * len(login_data.password) if login_data.password else 'N/A'}")
    logger.info(f"📦 전체 로그인 데이터: {json.dumps(login_data.dict(), ensure_ascii=False, indent=2)}")
    
    result = await auth_controller.login(login_data)
    
    logger.info("✅ === Auth Service 로그인 처리 완료 ===")
    logger.info(f"📤 응답 데이터: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    return result

@auth_router.post("/signup", summary="사용자 회원가입")
async def signup(signup_data: SignupRequest):
    """
    회원가입을 처리합니다.
    """
    import logging
    import json
    logger = logging.getLogger("auth_service")
    
    logger.info("📝 === Auth Service 회원가입 요청 ===")
    logger.info(f"🏭 업종: {signup_data.industry}")
    logger.info(f"📧 이메일: {signup_data.email}")
    logger.info(f"👤 이름: {signup_data.name}")
    logger.info(f"🎂 나이: {signup_data.age}")
    logger.info(f"🆔 아이디: {signup_data.auth_id}")
    logger.info(f"🔑 비밀번호: {'*' * len(signup_data.auth_pw) if signup_data.auth_pw else 'N/A'}")
    logger.info(f"📦 전체 회원가입 데이터: {json.dumps(signup_data.dict(), ensure_ascii=False, indent=2)}")
    
    result = await auth_controller.signup(signup_data)
    
    logger.info("✅ === Auth Service 회원가입 처리 완료 ===")
    logger.info(f"📤 응답 데이터: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    return result

# @auth_router.get("/google/login", summary="Google 로그인 시작")
# async def google_login(
#     redirect_uri: str = Query(
#         default="http://localhost:3000/dashboard",
#         description="로그인 후 리다이렉트할 URI (기본값: /dashboard)"
#     )
# ):
#     """
#     Google OAuth 로그인을 시작합니다.
#     리다이렉트 URI는 state 파라미터로 전달되어 콜백 시 다시 받게 됩니다.
#     """
#     return await google_controller.start_google_login(redirect_uri)

# @auth_router.get("/google/callback", summary="Google OAuth 콜백 처리")
# async def google_callback(
#     code: str = Query(..., description="Google OAuth 인증 코드"),
#     state: str = Query(..., description="로그인 시작 시 전달한 state 값")
# ):
#     """
#     Google OAuth 콜백을 처리합니다.
#     인증 코드를 받아 처리하고 세션 토큰을 쿠키에 설정한 후 리다이렉트합니다.
#     """
#     return await google_controller.handle_google_callback(code, state)

# @auth_router.post("/logout", summary="로그아웃")
# async def logout(session_token: str | None = Cookie(None)):
#     """
#     사용자를 로그아웃하고 인증 쿠키를 삭제합니다.
#     """
#     print(f"로그아웃 요청 - 받은 세션 토큰: {session_token}")
#     
#     # 로그아웃 응답 생성
#     response = JSONResponse({
#         "success": True,
#         "message": "로그아웃되었습니다."
#     })
#     
#     # 인증 쿠키 삭제
#     response.delete_cookie(
#         key="session_token",
#         path="/",
#         # domain 설정 제거 (로컬 환경)
#     )
#     
#     print("✅ 로그아웃 완료 - 인증 쿠키 삭제됨")
#     return response

# @auth_router.get("/profile", summary="사용자 프로필 조회")
# async def get_profile(session_token: str | None = Cookie(None)):
#     """
#     세션 토큰으로 사용자 프로필을 조회합니다.
#     세션 토큰이 없거나 유효하지 않으면 401 에러를 반환합니다.
#     """
#     print(f"프로필 요청 - 받은 세션 토큰: {session_token}")
#     
#     if not session_token:
#         raise HTTPException(status_code=401, detail="인증 쿠키가 없습니다.")
#     try:
#         return await google_controller.get_user_profile(session_token)
#     except Exception as e:
#         print(f"프로필 조회 오류: {e}")
#         raise HTTPException(status_code=401, detail=str(e))
from fastapi.responses import JSONResponse
from typing import Any, Dict
import httpx

class ResponseFactory:
    @staticmethod
    def success(data: Any = None, message: str = "Success") -> JSONResponse:
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": message,
                "data": data
            }
        )
    
    @staticmethod
    def error(message: str = "Error", status_code: int = 400) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "message": message
            }
        )
    
    @staticmethod
    def create_response(response: httpx.Response) -> JSONResponse:
        """httpx.Response를 FastAPI JSONResponse로 변환"""
        try:
            content = response.json()
        except:
            content = response.text
        
        return JSONResponse(
            status_code=response.status_code,
            content=content,
            headers=dict(response.headers)
        )

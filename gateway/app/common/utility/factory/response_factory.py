from fastapi.responses import JSONResponse
from typing import Any, Dict

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

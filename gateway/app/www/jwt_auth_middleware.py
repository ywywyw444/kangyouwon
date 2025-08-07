from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class AuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Skip auth for health check and docs
            if request.url.path in ["/health", "/docs", "/openapi.json"]:
                return await self.app(scope, receive, send)
            
            # Add your JWT validation logic here
            # For now, we'll just pass through
            logger.info(f"Processing request: {request.url.path}")
        
        return await self.app(scope, receive, send)

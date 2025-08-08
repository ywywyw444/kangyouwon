import logging
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log incoming requests."""

    def __init__(self, app, log_body: bool = False) -> None:
        super().__init__(app)
        self.log_body = log_body
        self.logger = logging.getLogger("request_logger")

    async def dispatch(self, request: Request, call_next: Callable):
        body_bytes = b""
        if self.log_body:
            body_bytes = await request.body()
            body_text = body_bytes.decode("utf-8", errors="replace")
            self.logger.info("%s %s Body: %s", request.method, request.url, body_text)

            async def receive() -> dict:  # pragma: no cover - internal
                return {"type": "http.request", "body": body_bytes, "more_body": False}

            request = Request(request.scope, receive)
        else:
            self.logger.info("%s %s", request.method, request.url)
        response = await call_next(request)
        return response
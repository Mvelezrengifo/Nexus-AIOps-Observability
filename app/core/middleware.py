"""
Custom middleware for FastAPI application.
Includes timing, request ID, and error handling.
"""

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import get_logger, log_context, clear_log_context
from app.core.exceptions import NexusException

logger = get_logger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Add a unique request ID to each request.
    Useful for tracing requests across logs and services.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Add to logging context
        log_context(request_id=request_id)

        # Process request
        response = await call_next(request)

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id

        # Clear context after request
        clear_log_context()

        return response


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Measure and log request processing time.
    Adds X-Process-Time header to response.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time
        process_time_ms = round(process_time * 1000, 2)

        # Add timing header
        response.headers["X-Process-Time"] = f"{process_time_ms}ms"

        # Log slow requests (>1s in development, >500ms in production)
        threshold = 0.5 if request.app.state.settings.is_production else 1.0
        if process_time > threshold:
            logger.warning(
                "Slow request detected",
                path=request.url.path,
                method=request.method,
                process_time_ms=process_time_ms,
            )

        return response


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """
    Global exception handler middleware.
    Catches all exceptions and returns structured JSON responses.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)

        except NexusException as exc:
            logger.error(
                "Application error",
                error_code=exc.error_code,
                message=exc.message,
                path=request.url.path,
            )

            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=exc.status_code,
                content=exc.to_dict(),
            )

        except Exception as exc:
            logger.exception(
                "Unhandled exception",
                path=request.url.path,
                method=request.method,
                error=str(exc),
            )

            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": {
                        "code": "INTERNAL_ERROR",
                        "message": "An unexpected error occurred",
                    },
                },
            )
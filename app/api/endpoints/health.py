"""
Health check endpoints.
"""

from fastapi import APIRouter

from app.config import settings
from app.core.logging import get_logger
from app.models.common import HealthResponse

router = APIRouter()
logger = get_logger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Basic health check.
    Returns service status and metadata.
    """
    logger.debug("Health check requested")

    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
        components={
            "api": "ok",
            "ai_engine": "configured" if settings.groq_api_key else "not_configured",
        },
    )


@router.get("/health/ready")
async def readiness_check() -> dict:
    """
    Readiness probe for Kubernetes/deployment.
    Checks if service is ready to receive traffic.
    """
    return {
        "ready": True,
        "checks": {
            "config": "ok",
            "ai_providers": {
                "groq": "available" if settings.groq_api_key else "unavailable",
                "openai": "available" if settings.openai_api_key else "unavailable",
            },
        },
    }


@router.get("/health/live")
async def liveness_check() -> dict:
    """
    Liveness probe for Kubernetes.
    Checks if service is alive (not deadlocked).
    """
    return {"alive": True}
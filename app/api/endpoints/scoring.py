"""
Operational Scoring endpoints.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.logging import get_logger
from app.models.scoring import ScoringRequest, ScoringResponse
from app.models.common import SuccessResponse
from app.services.scoring_service import ScoringService
from app.api.dependencies import CurrentUser, OptionalUser

router = APIRouter()
logger = get_logger(__name__)


@router.post("", response_model=ScoringResponse)
async def calculate_score(
        request: ScoringRequest,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: OptionalUser = None,
) -> ScoringResponse:
    """
    Calculate operational score for a service.

    Analyzes events and anomalies to generate a health score.
    """
    logger.info(
        "Calculating score",
        service=request.source_service,
        time_window=request.time_window_minutes,
    )

    service = ScoringService(db)

    result = await service.calculate_score(
        source_service=request.source_service,
        time_window_minutes=request.time_window_minutes,
    )

    return ScoringResponse(**result)


@router.post("/compare", response_model=dict)
async def compare_services(
        services: Annotated[list[str], Body(..., min_length=2)],
        db: Annotated[AsyncSession, Depends(get_db)],
        time_window_minutes: int = Query(60, ge=1, le=1440),
        current_user: OptionalUser = None,
) -> dict:
    """
    Compare scores across multiple services.

    Returns ranked comparison of service health.
    """
    logger.info("Comparing services", count=len(services))

    service = ScoringService(db)

    result = await service.get_service_comparison(
        services=services,
        time_window_minutes=time_window_minutes,
    )

    return result


@router.get("/quick/{source_service}")
async def quick_score(
        source_service: str,
        db: Annotated[AsyncSession, Depends(get_db)],
        time_window_minutes: int = Query(60, ge=1, le=1440),
        current_user: OptionalUser = None,
) -> dict:
    """
    Quick score calculation for a single service.
    Simplified response for dashboards.
    """
    service = ScoringService(db)

    result = await service.calculate_score(
        source_service=source_service,
        time_window_minutes=time_window_minutes,
    )

    return {
        "service": source_service,
        "score": float(result["overall_score"]),
        "risk_level": result["risk_level"],
        "recommendation": result["recommendations"][0] if result["recommendations"] else None,
    }
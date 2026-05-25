"""
AI Insights endpoints.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.logging import get_logger
from app.core.exceptions import NotFoundException
from app.models.insight import InsightCreate, InsightResponse, InsightFilter
from app.models.common import PaginatedResponse, SuccessResponse
from app.repositories.insight_repository import InsightRepository
from app.api.dependencies import CurrentUser, OptionalUser

router = APIRouter()
logger = get_logger(__name__)


@router.get("", response_model=PaginatedResponse[InsightResponse])
async def list_insights(
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: OptionalUser = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100),
        source_service: str | None = Query(None),
        recommendation_level: str | None = Query(None),
        is_acknowledged: bool | None = Query(None),
) -> PaginatedResponse[InsightResponse]:
    """
    List AI insights with optional filters.
    """
    logger.info("Listing insights", page=page, page_size=page_size)

    repo = InsightRepository(db)

    skip = (page - 1) * page_size

    # Get filtered results
    if source_service:
        insights = await repo.get_by_source_service(
            source_service, skip=skip, limit=page_size
        )
    elif recommendation_level:
        insights = await repo.get_by_recommendation_level(
            recommendation_level, skip=skip, limit=page_size
        )
    elif is_acknowledged is False:
        insights = await repo.get_unacknowledged(skip=skip, limit=page_size)
    else:
        insights = await repo.get_all(skip=skip, limit=page_size)

    total = await repo.count()

    return PaginatedResponse.create(
        data=[InsightResponse.model_validate(i) for i in insights],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{insight_id}", response_model=InsightResponse)
async def get_insight(
        insight_id: str,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: OptionalUser = None,
) -> InsightResponse:
    """
    Get a specific insight by ID.
    """
    repo = InsightRepository(db)
    insight = await repo.get_by_insight_id(insight_id)

    if insight is None:
        raise NotFoundException("Insight", insight_id)

    return InsightResponse.model_validate(insight)


@router.post("", response_model=InsightResponse, status_code=201)
async def create_insight(
        data: InsightCreate,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: CurrentUser,
) -> InsightResponse:
    """
    Create a new AI insight.
    Requires authentication.
    """
    logger.info(
        "Creating insight",
        type=data.insight_type,
        source=data.source_service,
        user=current_user["user_id"],
    )

    repo = InsightRepository(db)

    insight = await repo.create_insight(
        insight_type=data.insight_type,
        source_service=data.source_service,
        title=data.title,
        description=data.description,
        confidence_score=data.confidence_score,
        anomaly_type=data.anomaly_type,
        source_event_id=data.source_event_id,
        correlation_id=data.correlation_id,
        summary=data.summary,
        impact_score=data.impact_score,
        recommendation_level=data.recommendation_level,
        recommendation=data.recommendation,
        action_items=data.action_items,
        affected_resources=data.affected_resources,
        related_metrics=data.related_metrics,
        model_provider=data.model_provider,
        model_name=data.model_name,
    )

    logger.info("Insight created", insight_id=insight.insight_id)

    return InsightResponse.model_validate(insight)


@router.post("/{insight_id}/acknowledge", response_model=SuccessResponse)
async def acknowledge_insight(
        insight_id: str,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: CurrentUser,
) -> SuccessResponse:
    """
    Acknowledge an insight.
    Marks it as reviewed by the current user.
    """
    repo = InsightRepository(db)

    insight = await repo.acknowledge(
        insight_id=insight_id,
        acknowledged_by=current_user["user_id"],
    )

    if insight is None:
        raise NotFoundException("Insight", insight_id)

    logger.info(
        "Insight acknowledged",
        insight_id=insight_id,
        by=current_user["user_id"],
    )

    return SuccessResponse(
        message="Insight acknowledged successfully",
        data={"insight_id": insight_id},
    )
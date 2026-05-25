"""
Operational Events endpoints.
"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.logging import get_logger
from app.core.exceptions import NotFoundException
from app.models.event import EventCreate, EventResponse, EventFilter
from app.models.common import PaginatedResponse, SuccessResponse
from app.repositories.event_repository import EventRepository
from app.services.event_processor import EventProcessor
from app.api.dependencies import CurrentUser, OptionalUser

router = APIRouter()
logger = get_logger(__name__)


@router.get("", response_model=PaginatedResponse[EventResponse])
async def list_events(
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: OptionalUser = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100),
        source_service: str | None = Query(None),
        severity: str | None = Query(None),
        event_type: str | None = Query(None),
) -> PaginatedResponse[EventResponse]:
    """
    List operational events with optional filters.
    """
    logger.info("Listing events", page=page, page_size=page_size)

    repo = EventRepository(db)
    skip = (page - 1) * page_size

    if source_service:
        events = await repo.get_by_source_service(
            source_service, skip=skip, limit=page_size
        )
    elif severity:
        events = await repo.get_by_severity(
            severity, skip=skip, limit=page_size
        )
    else:
        events = await repo.get_all(skip=skip, limit=page_size)

    total = await repo.count()

    return PaginatedResponse.create(
        data=[EventResponse.model_validate(e) for e in events],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
        event_id: str,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: OptionalUser = None,
) -> EventResponse:
    """
    Get a specific event by ID.
    """
    repo = EventRepository(db)
    event = await repo.get_by_event_id(event_id)

    if event is None:
        raise NotFoundException("Event", event_id)

    return EventResponse.model_validate(event)


@router.get("/correlation/{correlation_id}", response_model=list[EventResponse])
async def get_events_by_correlation(
        correlation_id: str,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: OptionalUser = None,
) -> list[EventResponse]:
    """
    Get all events with the same correlation ID.
    Useful for tracing related events.
    """
    repo = EventRepository(db)
    events = await repo.get_by_correlation_id(correlation_id)

    return [EventResponse.model_validate(e) for e in events]


@router.post("", response_model=dict, status_code=201)
async def create_event(
        data: EventCreate,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: CurrentUser,
        generate_insight: bool = Query(
            False,
            description="Generate AI insight for high severity events",
        ),
) -> dict:
    """
    Create and process a new operational event.
    Optionally generates AI insight for HIGH/CRITICAL severity.
    """
    logger.info(
        "Creating event",
        type=data.event_type,
        source=data.source_service,
        severity=data.severity,
        user=current_user["user_id"],
    )

    processor = EventProcessor(db)

    result = await processor.process_event(
        event_data={
            "event_type": data.event_type,
            "event_name": data.event_name,
            "source_service": data.source_service,
            "description": data.description,
            "payload": data.payload,
            "severity": data.severity,
            "correlation_id": data.correlation_id,
            "parent_event_id": data.parent_event_id,
            "user_id": data.user_id or current_user["user_id"],
            "actor_type": data.actor_type,
            "tags": data.tags,
            "metadata": data.metadata,
        }
    )

    return result


@router.post("/batch", response_model=dict, status_code=201)
async def create_events_batch(
        events: list[EventCreate],
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: CurrentUser,
) -> dict:
    """
    Create multiple events in batch.
    Efficient for bulk ingestion.
    """
    logger.info(
        "Processing batch events",
        count=len(events),
        user=current_user["user_id"],
    )

    processor = EventProcessor(db)

    event_data_list = []
    for e in events:
        event_data_list.append({
            "event_type": e.event_type,
            "event_name": e.event_name,
            "source_service": e.source_service,
            "description": e.description,
            "payload": e.payload,
            "severity": e.severity,
            "correlation_id": e.correlation_id,
            "parent_event_id": e.parent_event_id,
            "user_id": e.user_id or current_user["user_id"],
            "actor_type": e.actor_type,
            "tags": e.tags,
            "metadata": e.metadata,
        })

    result = await processor.process_batch(event_data_list)

    return result


@router.get("/stats/summary")
async def get_event_stats(
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: OptionalUser = None,
        source_service: str | None = Query(None),
) -> dict:
    """
    Get event statistics summary.
    """
    repo = EventRepository(db)

    total = await repo.count()

    low = await repo.count_by_severity("LOW")
    medium = await repo.count_by_severity("MEDIUM")
    high = await repo.count_by_severity("HIGH")
    critical = await repo.count_by_severity("CRITICAL")

    result = {
        "total_events": total,
        "by_severity": {
            "LOW": low,
            "MEDIUM": medium,
            "HIGH": high,
            "CRITICAL": critical,
        },
    }

    if source_service:
        result["by_source"] = {
            source_service: await repo.count_by_source(source_service),
        }

    return result
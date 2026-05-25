"""
GraphQL schema definitions using Strawberry.
"""

import strawberry
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


@strawberry.type
class HealthStatus:
    """Health status type."""
    status: str
    service: str
    version: str
    environment: str


@strawberry.type
class Event:
    """Operational event type."""
    event_id: str
    event_type: str
    event_name: str
    source_service: str
    severity: str
    status: str
    description: Optional[str]
    correlation_id: Optional[str]
    created_at: datetime


@strawberry.type
class Insight:
    """AI insight type."""
    insight_id: str
    insight_type: str
    title: str
    description: str
    source_service: str
    confidence_score: float
    recommendation_level: str
    is_acknowledged: bool
    created_at: datetime


@strawberry.type
class ScoringResult:
    """Scoring result type."""
    metric_name: str
    value: float
    status: str
    contribution_percentage: float


@strawberry.type
class ServiceScore:
    """Service score type."""
    score_id: str
    source_service: str
    overall_score: float
    risk_level: str
    components: List[ScoringResult]


@strawberry.type
class Query:
    """GraphQL queries."""

    @strawberry.field
    async def health(self) -> HealthStatus:
        """Get service health status."""
        from app.config import settings

        return HealthStatus(
            status="healthy",
            service=settings.app_name,
            version=settings.app_version,
            environment=settings.app_env,
        )

    @strawberry.field
    async def event(self, event_id: str) -> Optional[Event]:
        """Get event by ID."""
        from app.db.database import get_db_context
        from app.repositories.event_repository import EventRepository

        async with get_db_context() as db:
            repo = EventRepository(db)
            event = await repo.get_by_event_id(event_id)

            if event is None:
                return None

            return Event(
                event_id=event.event_id,
                event_type=event.event_type,
                event_name=event.event_name,
                source_service=event.source_service,
                severity=event.severity,
                status=event.status,
                description=event.description,
                correlation_id=event.correlation_id,
                created_at=event.created_at,
            )

    @strawberry.field
    async def events(
            self,
            source_service: Optional[str] = None,
            severity: Optional[str] = None,
            limit: int = 20,
    ) -> List[Event]:
        """List events with optional filters."""
        from app.db.database import get_db_context
        from app.repositories.event_repository import EventRepository

        async with get_db_context() as db:
            repo = EventRepository(db)

            if source_service:
                events = await repo.get_by_source_service(
                    source_service, limit=limit
                )
            elif severity:
                events = await repo.get_by_severity(severity, limit=limit)
            else:
                events = await repo.get_all(limit=limit)

            return [
                Event(
                    event_id=e.event_id,
                    event_type=e.event_type,
                    event_name=e.event_name,
                    source_service=e.source_service,
                    severity=e.severity,
                    status=e.status,
                    description=e.description,
                    correlation_id=e.correlation_id,
                    created_at=e.created_at,
                )
                for e in events
            ]

    @strawberry.field
    async def insight(self, insight_id: str) -> Optional[Insight]:
        """Get insight by ID."""
        from app.db.database import get_db_context
        from app.repositories.insight_repository import InsightRepository

        async with get_db_context() as db:
            repo = InsightRepository(db)
            insight = await repo.get_by_insight_id(insight_id)

            if insight is None:
                return None

            return Insight(
                insight_id=insight.insight_id,
                insight_type=insight.insight_type,
                title=insight.title,
                description=insight.description,
                source_service=insight.source_service,
                confidence_score=float(insight.confidence_score),
                recommendation_level=insight.recommendation_level,
                is_acknowledged=insight.is_acknowledged,
                created_at=insight.created_at,
            )

    @strawberry.field
    async def insights(
            self,
            source_service: Optional[str] = None,
            limit: int = 20,
    ) -> List[Insight]:
        """List insights with optional filters."""
        from app.db.database import get_db_context
        from app.repositories.insight_repository import InsightRepository

        async with get_db_context() as db:
            repo = InsightRepository(db)

            if source_service:
                insights = await repo.get_by_source_service(
                    source_service, limit=limit
                )
            else:
                insights = await repo.get_all(limit=limit)

            return [
                Insight(
                    insight_id=i.insight_id,
                    insight_type=i.insight_type,
                    title=i.title,
                    description=i.description,
                    source_service=i.source_service,
                    confidence_score=float(i.confidence_score),
                    recommendation_level=i.recommendation_level,
                    is_acknowledged=i.is_acknowledged,
                    created_at=i.created_at,
                )
                for i in insights
            ]

    @strawberry.field
    async def service_score(
            self,
            source_service: str,
            time_window_minutes: int = 60,
    ) -> ServiceScore:
        """Calculate score for a service."""
        from app.db.database import get_db_context
        from app.services.scoring_service import ScoringService

        async with get_db_context() as db:
            service = ScoringService(db)
            result = await service.calculate_score(
                source_service=source_service,
                time_window_minutes=time_window_minutes,
            )

            return ServiceScore(
                score_id=result["score_id"],
                source_service=result["source_service"],
                overall_score=float(result["overall_score"]),
                risk_level=result["risk_level"],
                components=[
                    ScoringResult(
                        metric_name=c["metric_name"],
                        value=float(c["value"]),
                        status=c["status"],
                        contribution_percentage=float(c["contribution_percentage"]),
                    )
                    for c in result["components"]
                ],
            )


# Create schema
schema = strawberry.Schema(query=Query)
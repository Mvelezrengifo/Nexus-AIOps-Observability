"""
GraphQL resolvers for complex queries and mutations.
"""

from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.repositories.event_repository import EventRepository
from app.repositories.insight_repository import InsightRepository
from app.repositories.anomaly_repository import AnomalyRepository
from app.repositories.metric_repository import MetricRepository
from app.services.correlation_service import CorrelationService
from app.services.scoring_service import ScoringService
from app.services.prediction_service import PredictionService

logger = get_logger(__name__)


class EventResolvers:
    """Resolvers for event-related queries."""

    @staticmethod
    async def get_events_by_time_range(
            session: AsyncSession,
            start_time: datetime,
            end_time: datetime,
            limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get events within time range."""
        repo = EventRepository(session)
        events = await repo.get_by_time_range(
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )
        return [e.to_dict() for e in events]

    @staticmethod
    async def get_event_stats(
            session: AsyncSession,
            source_service: str | None = None,
    ) -> dict[str, Any]:
        """Get event statistics."""
        repo = EventRepository(session)

        total = await repo.count()
        low = await repo.count_by_severity("LOW")
        medium = await repo.count_by_severity("MEDIUM")
        high = await repo.count_by_severity("HIGH")
        critical = await repo.count_by_severity("CRITICAL")

        stats = {
            "total": total,
            "by_severity": {
                "LOW": low,
                "MEDIUM": medium,
                "HIGH": high,
                "CRITICAL": critical,
            },
        }

        if source_service:
            stats["by_source"] = {
                source_service: await repo.count_by_source(source_service),
            }

        return stats


class InsightResolvers:
    """Resolvers for insight-related queries."""

    @staticmethod
    async def get_high_confidence_insights(
            session: AsyncSession,
            min_confidence: float = 0.8,
            limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Get insights with high confidence."""
        from decimal import Decimal

        repo = InsightRepository(session)
        insights = await repo.get_high_confidence(
            min_confidence=Decimal(str(min_confidence)),
            limit=limit,
        )
        return [i.to_dict() for i in insights]

    @staticmethod
    async def get_unacknowledged_count(session: AsyncSession) -> int:
        """Count unacknowledged insights."""
        from sqlalchemy import select, func
        from app.db.models.ai_insight import AIInsight

        result = await session.execute(
            select(func.count())
            .where(AIInsight.is_acknowledged == False)
        )
        return result.scalar_one()


class CorrelationResolvers:
    """Resolvers for correlation queries."""

    @staticmethod
    async def analyze_correlations(
            session: AsyncSession,
            source_service: str,
            time_window_minutes: int = 60,
    ) -> dict[str, Any]:
        """Analyze event correlations."""
        service = CorrelationService(session)
        return await service.correlate_events(
            source_service=source_service,
            time_window_minutes=time_window_minutes,
        )


class ScoringResolvers:
    """Resolvers for scoring queries."""

    @staticmethod
    async def compare_services(
            session: AsyncSession,
            services: list[str],
            time_window_minutes: int = 60,
    ) -> dict[str, Any]:
        """Compare scores across services."""
        service = ScoringService(session)
        return await service.get_service_comparison(
            services=services,
            time_window_minutes=time_window_minutes,
        )


class PredictionResolvers:
    """Resolvers for prediction queries."""

    @staticmethod
    async def get_prediction(
            session: AsyncSession,
            prediction_type: str,
            source_service: str,
            time_horizon_hours: int = 24,
    ) -> dict[str, Any]:
        """Generate prediction."""
        service = PredictionService(session)
        return await service.predict(
            prediction_type=prediction_type,
            source_service=source_service,
            time_horizon_hours=time_horizon_hours,
        )
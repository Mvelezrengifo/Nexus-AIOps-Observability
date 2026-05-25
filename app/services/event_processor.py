"""
Event Processor - Processes and enriches operational events.
"""

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.repositories.event_repository import EventRepository
from app.repositories.insight_repository import InsightRepository
from app.services.ai_engine import get_ai_engine

logger = get_logger(__name__)


class EventProcessor:
    """
    Service for processing operational events.

    Handles event enrichment, classification, and insight generation.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.event_repo = EventRepository(session)
        self.insight_repo = InsightRepository(session)

    async def process_event(
            self,
            event_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Process an incoming event.

        Args:
            event_data: Raw event data

        Returns:
            Processing result with created event
        """
        # Create event
        event = await self.event_repo.create_event(**event_data)

        logger.info(
            "Event created",
            event_id=event.event_id,
            type=event.event_type,
            source=event.source_service,
        )

        # Enrich event
        enriched = await self._enrich_event(event)

        # Generate insight if high severity
        insight = None
        if event.severity in ("HIGH", "CRITICAL"):
            insight = await self._generate_insight_for_event(event)

        return {
            "event": event.to_dict(),
            "enriched": enriched,
            "insight_generated": insight is not None,
            "insight": insight,
        }

    async def process_batch(
            self,
            events: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Process multiple events in batch.

        Args:
            events: List of event data

        Returns:
            Batch processing results
        """
        results = []
        successful = 0
        failed = 0

        for event_data in events:
            try:
                result = await self.process_event(event_data)
                results.append(result)
                successful += 1
            except Exception as e:
                logger.error(
                    "Failed to process event",
                    error=str(e),
                    event_data=event_data,
                )
                failed += 1

        return {
            "batch_id": str(uuid4()),
            "total": len(events),
            "successful": successful,
            "failed": failed,
            "results": results,
            "processed_at": datetime.utcnow().isoformat(),
        }

    async def _enrich_event(self, event: Any) -> dict[str, Any]:
        """Enrich event with additional context."""
        enrichment = {
            "original_severity": event.severity,
            "enrichment_applied": [],
        }

        # Auto-escalate based on patterns
        if event.event_type == "ERROR" and event.severity == "MEDIUM":
            # Check for repeated errors
            recent = await self.event_repo.get_by_source_service(
                event.source_service, limit=10
            )

            error_count = sum(
                1 for e in recent
                if e.event_type == "ERROR" and e.severity == "MEDIUM"
            )

            if error_count >= 3:
                enrichment["escalated_severity"] = "HIGH"
                enrichment["enrichment_applied"].append("severity_escalation")

                # Update event
                await self.event_repo.update(
                    event.id,
                    {"severity": "HIGH"},
                )

        # Add correlation hints
        if event.correlation_id:
            enrichment["has_correlation"] = True
            enrichment["enrichment_applied"].append("correlation_linked")

        return enrichment

    async def _generate_insight_for_event(
            self,
            event: Any,
    ) -> dict[str, Any] | None:
        """Generate AI insight for a significant event."""
        try:
            ai_engine = await get_ai_engine()

            context = {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "event_name": event.event_name,
                "source_service": event.source_service,
                "severity": event.severity,
                "description": event.description,
                "payload": event.payload,
                "occurred_at": event.occurred_at.isoformat() if event.occurred_at else None,
            }

            ai_result = await ai_engine.generate_insight(
                context,
                insight_type="ANOMALY_DETECTION",
            )

            # Create insight record
            insight = await self.insight_repo.create_insight(
                insight_type="ANOMALY_DETECTION",
                source_service=event.source_service,
                source_event_id=event.event_id,
                title=ai_result.get("title", "Event Analysis"),
                description=ai_result.get("description", ""),
                confidence_score=ai_result.get("confidence_score", 0.7),
                anomaly_type=ai_result.get("anomaly_type"),
                recommendation_level=ai_result.get("recommendation_level", "INFO"),
                recommendation=ai_result.get("recommendation"),
                action_items=ai_result.get("action_items", []),
                model_provider=ai_result.get("model_provider"),
                model_name=ai_result.get("model_name"),
            )

            logger.info(
                "Insight generated for event",
                event_id=event.event_id,
                insight_id=insight.insight_id,
            )

            return insight.to_dict()

        except Exception as e:
            logger.error(
                "Failed to generate insight for event",
                event_id=event.event_id,
                error=str(e),
            )
            return None

    async def mark_processed(self, event_id: str) -> bool:
        """Mark an event as processed."""
        event = await self.event_repo.get_by_event_id(event_id)

        if event is None:
            return False

        await self.event_repo.update(
            event.id,
            {
                "status": "COMPLETED",
                "processed_at": datetime.utcnow().isoformat(),
            },
        )

        return True

    async def get_pending_events(
            self,
            limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get all pending events."""
        events = await self.event_repo.get_by_field("status", "PENDING")

        if events is None:
            return []

        # Get multiple pending
        from sqlalchemy import select
        from app.db.models.operational_event import OperationalEvent

        result = await self.session.execute(
            select(OperationalEvent)
            .where(OperationalEvent.status == "PENDING")
            .order_by(OperationalEvent.created_at.asc())
            .limit(limit)
        )

        events = result.scalars().all()

        return [e.to_dict() for e in events]
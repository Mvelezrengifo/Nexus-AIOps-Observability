"""
Correlation Service - Analyzes relationships between events.
"""

from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.repositories.event_repository import EventRepository

logger = get_logger(__name__)


class CorrelationService:
    """
    Service for correlating operational events.

    Identifies patterns and relationships between events
    to provide meaningful insights.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.event_repo = EventRepository(session)

    async def correlate_events(
            self,
            source_service: str,
            time_window_minutes: int = 60,
    ) -> dict[str, Any]:
        """
        Find correlations between events from a service.

        Args:
            source_service: Service to analyze
            time_window_minutes: Time window for correlation

        Returns:
            Correlation analysis results
        """
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=time_window_minutes)

        # Get events in time window
        events = await self.event_repo.get_by_time_range(
            start_time=start_time,
            end_time=end_time,
            limit=500,
        )

        # Filter by service
        service_events = [
            e for e in events if e.source_service == source_service
        ]

        correlations = {
            "correlation_id": str(uuid4()),
            "source_service": source_service,
            "time_window": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
            },
            "total_events": len(service_events),
            "correlations": [],
            "patterns": [],
        }

        if not service_events:
            return correlations

        # Group by event type
        type_groups: dict[str, list] = {}
        for event in service_events:
            if event.event_type not in type_groups:
                type_groups[event.event_type] = []
            type_groups[event.event_type].append(event)

        # Find sequential patterns
        patterns = self._find_sequential_patterns(service_events)
        correlations["patterns"] = patterns

        # Find related events (same correlation_id)
        related = await self._find_related_events(service_events)
        correlations["correlations"] = related

        logger.info(
            "Correlation analysis complete",
            source_service=source_service,
            total_events=len(service_events),
            patterns_found=len(patterns),
        )

        return correlations

    async def correlate_by_type(
            self,
            event_type: str,
            time_window_hours: int = 24,
    ) -> dict[str, Any]:
        """
        Find correlations by event type.

        Args:
            event_type: Type of events to correlate
            time_window_hours: Time window in hours

        Returns:
            Correlation results
        """
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=time_window_hours)

        events = await self.event_repo.get_by_time_range(
            start_time=start_time,
            end_time=end_time,
            limit=1000,
        )

        filtered = [e for e in events if e.event_type == event_type]

        # Group by source service
        service_distribution: dict[str, int] = {}
        for event in filtered:
            service = event.source_service
            service_distribution[service] = service_distribution.get(service, 0) + 1

        # Analyze severity distribution
        severity_distribution: dict[str, int] = {}
        for event in filtered:
            sev = event.severity
            severity_distribution[sev] = severity_distribution.get(sev, 0) + 1

        return {
            "event_type": event_type,
            "time_window_hours": time_window_hours,
            "total_events": len(filtered),
            "service_distribution": service_distribution,
            "severity_distribution": severity_distribution,
            "most_common_service": max(
                service_distribution.items(),
                key=lambda x: x[1],
                default=(None, 0),
            )[0],
        }

    def _find_sequential_patterns(
            self,
            events: list[Any],
    ) -> list[dict[str, Any]]:
        """Find sequential event patterns."""
        patterns = []

        if len(events) < 2:
            return patterns

        # Sort by occurrence time
        sorted_events = sorted(events, key=lambda e: e.occurred_at)

        # Look for repeated sequences
        for i in range(len(sorted_events) - 1):
            current = sorted_events[i]
            next_event = sorted_events[i + 1]

            time_diff = (next_event.occurred_at - current.occurred_at).total_seconds()

            # If events happen within 5 minutes, consider them related
            if time_diff < 300:
                patterns.append({
                    "event_1": {
                        "type": current.event_type,
                        "id": current.event_id,
                    },
                    "event_2": {
                        "type": next_event.event_type,
                        "id": next_event.event_id,
                    },
                    "time_diff_seconds": time_diff,
                    "pattern_type": "SEQUENTIAL",
                })

        return patterns

    async def _find_related_events(
            self,
            events: list[Any],
    ) -> list[dict[str, Any]]:
        """Find events with same correlation_id."""
        correlation_groups: dict[str, list] = {}

        for event in events:
            if event.correlation_id:
                if event.correlation_id not in correlation_groups:
                    correlation_groups[event.correlation_id] = []
                correlation_groups[event.correlation_id].append(event)

        # Return groups with more than one event
        related = []
        for corr_id, group in correlation_groups.items():
            if len(group) > 1:
                related.append({
                    "correlation_id": corr_id,
                    "event_count": len(group),
                    "event_types": list(set(e.event_type for e in group)),
                    "services": list(set(e.source_service for e in group)),
                })

        return related
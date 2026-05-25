"""
Repository for Operational Events.
"""

from datetime import datetime
from typing import Any

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.operational_event import OperationalEvent
from app.repositories.base import BaseRepository


class EventRepository(BaseRepository[OperationalEvent]):
    """
    Repository for operational events.

    Provides specialized queries for event data.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(OperationalEvent, session)

    async def get_by_event_id(self, event_id: str) -> OperationalEvent | None:
        """
        Get event by its unique event_id.

        Args:
            event_id: Unique event identifier

        Returns:
            Event instance or None
        """
        return await self.get_by_field("event_id", event_id)

    async def get_by_correlation_id(
            self,
            correlation_id: str,
    ) -> list[OperationalEvent]:
        """
        Get all events with same correlation ID.

        Args:
            correlation_id: Correlation identifier

        Returns:
            List of related events
        """
        result = await self.session.execute(
            select(OperationalEvent)
            .where(OperationalEvent.correlation_id == correlation_id)
            .order_by(OperationalEvent.occurred_at)
        )
        return list(result.scalars().all())

    async def get_by_source_service(
            self,
            source_service: str,
            skip: int = 0,
            limit: int = 100,
    ) -> list[OperationalEvent]:
        """
        Get events by source service.

        Args:
            source_service: Service name
            skip: Records to skip
            limit: Max records

        Returns:
            List of events
        """
        result = await self.session.execute(
            select(OperationalEvent)
            .where(OperationalEvent.source_service == source_service)
            .order_by(OperationalEvent.occurred_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_severity(
            self,
            severity: str,
            skip: int = 0,
            limit: int = 100,
    ) -> list[OperationalEvent]:
        """
        Get events by severity level.

        Args:
            severity: Severity level (LOW, MEDIUM, HIGH, CRITICAL)
            skip: Records to skip
            limit: Max records

        Returns:
            List of events
        """
        result = await self.session.execute(
            select(OperationalEvent)
            .where(OperationalEvent.severity == severity)
            .order_by(OperationalEvent.occurred_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_time_range(
            self,
            start_time: datetime,
            end_time: datetime,
            skip: int = 0,
            limit: int = 100,
    ) -> list[OperationalEvent]:
        """
        Get events within a time range.

        Args:
            start_time: Start of range
            end_time: End of range
            skip: Records to skip
            limit: Max records

        Returns:
            List of events
        """
        result = await self.session.execute(
            select(OperationalEvent)
            .where(
                and_(
                    OperationalEvent.occurred_at >= start_time,
                    OperationalEvent.occurred_at <= end_time,
                )
            )
            .order_by(OperationalEvent.occurred_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create_event(
            self,
            event_type: str,
            event_name: str,
            source_service: str,
            **kwargs: Any,
    ) -> OperationalEvent:
        """
        Create a new operational event.

        Args:
            event_type: Type of event
            event_name: Name of event
            source_service: Source service
            **kwargs: Additional fields

        Returns:
            Created event
        """
        data = {
            "event_id": self._generate_uuid(),
            "event_type": event_type,
            "event_name": event_name,
            "source_service": source_service,
            **kwargs,
        }

        return await self.create(data)

    async def count_by_severity(self, severity: str) -> int:
        """
        Count events by severity.

        Args:
            severity: Severity level

        Returns:
            Count of events
        """
        from sqlalchemy import func

        result = await self.session.execute(
            select(func.count())
            .where(OperationalEvent.severity == severity)
        )
        return result.scalar_one()

    async def count_by_source(self, source_service: str) -> int:
        """
        Count events by source service.

        Args:
            source_service: Service name

        Returns:
            Count of events
        """
        from sqlalchemy import func

        result = await self.session.execute(
            select(func.count())
            .where(OperationalEvent.source_service == source_service)
        )
        return result.scalar_one()
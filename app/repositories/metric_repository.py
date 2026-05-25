"""
Repository for Metrics.
"""

from datetime import datetime
from typing import Any

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.metric import Metric
from app.repositories.base import BaseRepository


class MetricRepository(BaseRepository[Metric]):
    """Repository for operational metrics."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Metric, session)

    async def get_by_metric_id(self, metric_id: str) -> Metric | None:
        """Get metric by its unique ID."""
        return await self.get_by_field("metric_id", metric_id)

    async def get_by_name(
            self,
            metric_name: str,
            skip: int = 0,
            limit: int = 100,
    ) -> list[Metric]:
        """Get metrics by name."""
        result = await self.session.execute(
            select(Metric)
            .where(Metric.metric_name == metric_name)
            .order_by(Metric.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_source_service(
            self,
            source_service: str,
            skip: int = 0,
            limit: int = 100,
    ) -> list[Metric]:
        """Get metrics by source service."""
        result = await self.session.execute(
            select(Metric)
            .where(Metric.source_service == source_service)
            .order_by(Metric.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_category(
            self,
            category: str,
            skip: int = 0,
            limit: int = 100,
    ) -> list[Metric]:
        """Get metrics by category."""
        result = await self.session.execute(
            select(Metric)
            .where(Metric.category == category)
            .order_by(Metric.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_latest_by_name(
            self,
            metric_name: str,
            source_service: str | None = None,
    ) -> Metric | None:
        """Get the most recent metric by name."""
        query = select(Metric).where(Metric.metric_name == metric_name)

        if source_service:
            query = query.where(Metric.source_service == source_service)

        result = await self.session.execute(
            query.order_by(Metric.created_at.desc()).limit(1)
        )
        return result.scalar_one_or_none()

    async def get_by_time_range(
            self,
            metric_name: str,
            start_time: datetime,
            end_time: datetime,
            skip: int = 0,
            limit: int = 100,
    ) -> list[Metric]:
        """Get metrics within a time range."""
        result = await self.session.execute(
            select(Metric)
            .where(
                and_(
                    Metric.metric_name == metric_name,
                    Metric.created_at >= start_time,
                    Metric.created_at <= end_time,
                )
            )
            .order_by(Metric.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create_metric(
            self,
            metric_name: str,
            metric_type: str,
            source_service: str,
            value: Any,
            **kwargs: Any,
    ) -> Metric:
        """Create a new metric."""
        from decimal import Decimal

        data = {
            "metric_id": self._generate_uuid(),
            "metric_name": metric_name,
            "metric_type": metric_type,
            "source_service": source_service,
            "value": Decimal(str(value)),
            **kwargs,
        }

        return await self.create(data)
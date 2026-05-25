"""
Repository for Anomaly Logs.
"""

from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.anomaly_log import AnomalyLog
from app.repositories.base import BaseRepository


class AnomalyRepository(BaseRepository[AnomalyLog]):
    """Repository for anomaly logs."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(AnomalyLog, session)

    async def get_by_anomaly_id(self, anomaly_id: str) -> AnomalyLog | None:
        """Get anomaly by its unique ID."""
        return await self.get_by_field("anomaly_id", anomaly_id)

    async def get_by_status(
            self,
            status: str,
            skip: int = 0,
            limit: int = 100,
    ) -> list[AnomalyLog]:
        """Get anomalies by status."""
        result = await self.session.execute(
            select(AnomalyLog)
            .where(AnomalyLog.status == status)
            .order_by(AnomalyLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_severity(
            self,
            severity: str,
            skip: int = 0,
            limit: int = 100,
    ) -> list[AnomalyLog]:
        """Get anomalies by severity."""
        result = await self.session.execute(
            select(AnomalyLog)
            .where(AnomalyLog.severity == severity)
            .order_by(AnomalyLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_source_service(
            self,
            source_service: str,
            skip: int = 0,
            limit: int = 100,
    ) -> list[AnomalyLog]:
        """Get anomalies by source service."""
        result = await self.session.execute(
            select(AnomalyLog)
            .where(AnomalyLog.source_service == source_service)
            .order_by(AnomalyLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_open_anomalies(
            self,
            skip: int = 0,
            limit: int = 100,
    ) -> list[AnomalyLog]:
        """Get all open (non-resolved) anomalies."""
        result = await self.session.execute(
            select(AnomalyLog)
            .where(AnomalyLog.status != "RESOLVED")
            .where(AnomalyLog.status != "FALSE_POSITIVE")
            .order_by(AnomalyLog.severity.desc(), AnomalyLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def resolve(
            self,
            anomaly_id: str,
            resolved_by: str,
            notes: str | None = None,
    ) -> AnomalyLog | None:
        """Mark an anomaly as resolved."""
        anomaly = await self.get_by_anomaly_id(anomaly_id)

        if anomaly is None:
            return None

        return await self.update(
            anomaly.id,
            {
                "status": "RESOLVED",
                "resolved_by": resolved_by,
                "resolved_at": datetime.utcnow().isoformat(),
                "resolution_notes": notes,
            },
        )

    async def create_anomaly(
            self,
            anomaly_type: str,
            source_service: str,
            description: str,
            severity: str = "MEDIUM",
            **kwargs: Any,
    ) -> AnomalyLog:
        """Create a new anomaly log."""
        data = {
            "anomaly_id": self._generate_uuid(),
            "anomaly_type": anomaly_type,
            "source_service": source_service,
            "description": description,
            "severity": severity,
            **kwargs,
        }

        return await self.create(data)
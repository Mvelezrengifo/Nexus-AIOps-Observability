"""
Service Health model - tracks health status of microservices.
"""

from decimal import Decimal
from enum import Enum
from typing import Any

from sqlalchemy import String, Text, JSON, Numeric, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class HealthStatus(str, Enum):
    """Service health status."""
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


class ServiceHealth(Base):
    """
    Service Health table.

    Tracks real-time health status of all microservices.
    """

    __tablename__ = "service_health"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Service identification
    service_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
    )
    service_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # Health status
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=HealthStatus.UNKNOWN.value,
        index=True,
    )

    # Version info
    version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    build_number: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Metrics
    uptime_percentage: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2), nullable=True
    )
    response_time_ms: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    error_rate: Mapped[Decimal | None] = mapped_column(Numeric(5, 4), nullable=True)

    # Instance info
    instance_count: Mapped[int | None] = mapped_column(nullable=True)
    active_connections: Mapped[int | None] = mapped_column(nullable=True)

    # Dependencies
    dependencies: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # Last check
    last_check_at: Mapped[str | None] = mapped_column(nullable=True)
    last_healthy_at: Mapped[str | None] = mapped_column(nullable=True)

    # Error info
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_details: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # Metadata
    endpoint: Mapped[str | None] = mapped_column(String(500), nullable=True)
    metadata: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # Indexes
    __table_args__ = (
        Index("ix_service_health_name_status", "service_name", "status"),
        Index("ix_service_health_status_check", "status", "last_check_at"),
    )

    def __repr__(self) -> str:
        return f"<ServiceHealth(id={self.id}, service={self.service_name}, status={self.status})>"
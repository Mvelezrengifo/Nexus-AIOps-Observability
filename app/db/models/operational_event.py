"""
Operational Event model - stores system and business events.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from sqlalchemy import String, Text, JSON, DateTime, Index, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EventSeverity(str, Enum):
    """Event severity levels."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class EventStatus(str, Enum):
    """Event processing status."""
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class OperationalEvent(Base):
    """
    Operational events table.

    Stores all operational events for monitoring, correlation, and analysis.
    """

    __tablename__ = "operational_events"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Event identification
    event_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
    )

    # Event metadata
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    event_name: Mapped[str] = mapped_column(String(200), nullable=False)
    source_service: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # Event content
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # Severity and status
    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=EventSeverity.LOW.value,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=EventStatus.PENDING.value,
        index=True,
    )

    # Timing
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Correlation (for linking related events)
    correlation_id: Mapped[str | None] = mapped_column(
        String(36),
        nullable=True,
        index=True,
    )
    parent_event_id: Mapped[str | None] = mapped_column(String(36), nullable=True)

    # User/actor context
    user_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    actor_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Additional metadata
    tags: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    # =====================================================================
    # CORRECCIÓN: Se renombra la propiedad de python a 'event_metadata'
    # pero mapea a la columna "metadata" en la BD para que no choque con SQLAlchemy
    # =====================================================================
    event_metadata: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSON, nullable=True)

    # Indexes for common queries (Corregido 'created_at' por 'occurred_at')
    __table_args__ = (
        Index("ix_operational_events_source_severity", "source_service", "severity"),
        Index("ix_operational_events_type_occurred", "event_type", "occurred_at"),
        Index("ix_operational_events_status_occurred", "status", "occurred_at"),
    )

    def __repr__(self) -> str:
        return f"<OperationalEvent(id={self.id}, type={self.event_type}, severity={self.severity})>"
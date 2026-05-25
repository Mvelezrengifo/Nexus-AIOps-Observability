"""
Anomaly Log model - stores detected anomalies for tracking.
"""

from decimal import Decimal
from enum import Enum
from typing import Any

from sqlalchemy import String, Text, JSON, Numeric, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AnomalyStatus(str, Enum):
    """Anomaly tracking status."""
    DETECTED = "DETECTED"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    IGNORED = "IGNORED"


class AnomalyLog(Base):
    """
    Anomaly Logs table.

    Tracks all detected anomalies and their resolution status.
    """

    __tablename__ = "anomaly_logs"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Anomaly identification
    anomaly_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
    )

    # Classification
    anomaly_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Source
    source_service: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    source_metric: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Detection details
    detected_value: Mapped[Decimal | None] = mapped_column(Numeric(20, 6), nullable=True)
    expected_value: Mapped[Decimal | None] = mapped_column(Numeric(20, 6), nullable=True)
    deviation_percentage: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 4), nullable=True
    )

    # Severity
    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="MEDIUM",
        index=True,
    )

    # Content
    description: Mapped[str] = mapped_column(Text, nullable=False)
    context: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    raw_data: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # Related insight
    insight_id: Mapped[str | None] = mapped_column(String(36), nullable=True)

    # Status tracking
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default=AnomalyStatus.DETECTED.value,
        index=True,
    )
    resolved_at: Mapped[str | None] = mapped_column(nullable=True)
    resolved_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    resolution_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Time window
    detection_window_start: Mapped[str | None] = mapped_column(nullable=True)
    detection_window_end: Mapped[str | None] = mapped_column(nullable=True)

    # Indexes
    __table_args__ = (
        Index("ix_anomaly_logs_type_status", "anomaly_type", "status"),
        Index("ix_anomaly_logs_source_severity", "source_service", "severity"),
    )

    def __repr__(self) -> str:
        return f"<AnomalyLog(id={self.id}, type={self.anomaly_type}, status={self.status})>"
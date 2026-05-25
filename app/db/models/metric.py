"""
Database model for operational metrics.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    DateTime,
    Boolean,
    Text,
    Index,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB

from app.db.base import Base


class Metric(Base):
    """
    ORM model for storing operational metrics.

    Supports time-series data, tagging, and contextual metadata
    for observability and alerting systems.
    """

    __tablename__ = "metrics"

    # Primary key
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Core metric fields
    metric_name = Column(String(100), nullable=False, index=True)  # e.g., "cpu_usage", "request_latency"
    metric_value = Column(Float, nullable=False)  # The actual measured value
    metric_unit = Column(String(20), nullable=False, default="")  # e.g., "%", "ms", "bytes"

    # Context & tagging
    service_name = Column(String(100), nullable=False, index=True)  # Source service
    environment = Column(String(20), nullable=False, default="production")  # dev/staging/prod
    host = Column(String(100), nullable=True)  # Optional: specific host/instance
    tags = Column(JSONB, default=dict, nullable=False)  # Flexible key-value tags for filtering

    # 🔧 FIX: Renamed 'metadata' → 'extra_metadata' (reserved word in SQLAlchemy)
    extra_metadata = Column(JSONB, default=dict, nullable=False)  # Additional structured context

    # Temporal fields
    timestamp = Column(DateTime(timezone=True), nullable=False, default=func.now(), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Quality & status
    is_valid = Column(Boolean, default=True, index=True)  # Flag for data quality checks
    source_type = Column(String(50), nullable=False, default="automatic")  # automatic/manual/derived

    # Optional description for human readability
    description = Column(Text, nullable=True)

    # Indexes for common query patterns
    __table_args__ = (
        # Composite index for time-range queries by service
        Index("ix_metrics_service_timestamp", "service_name", "timestamp"),
        # Index for tag-based filtering (GIN for JSONB)
        Index("ix_metrics_tags", "tags", postgresql_using="gin"),
        # Index for metric name + environment (common dashboard filter)
        Index("ix_metrics_name_env", "metric_name", "environment"),
    )

    def __repr__(self) -> str:
        return (
            f"<Metric(id={self.id}, name={self.metric_name}, "
            f"value={self.metric_value}{self.metric_unit}, "
            f"service={self.service_name}, ts={self.timestamp})>"
        )

    def to_dict(self) -> dict:
        """
        Convert metric to dictionary for API responses.

        Returns:
            dict: Serializable representation
        """
        return {
            "id": str(self.id),
            "metric_name": self.metric_name,
            "metric_value": self.metric_value,
            "metric_unit": self.metric_unit,
            "service_name": self.service_name,
            "environment": self.environment,
            "host": self.host,
            "tags": self.tags,
            "extra_metadata": self.extra_metadata,  # 🔧 Renamed field
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "is_valid": self.is_valid,
            "source_type": self.source_type,
            "description": self.description,
        }

    @classmethod
    def create_sample(
            cls,
            metric_name: str,
            value: float,
            service: str,
            unit: str = "",
            tags: Optional[dict] = None,
            extra_metadata: Optional[dict] = None,  # 🔧 Renamed parameter
            **kwargs
    ) -> "Metric":
        """
        Factory method for creating sample metrics (useful for testing/seeding).

        Args:
            metric_name: Name of the metric
            value: Numeric value
            service: Source service name
            unit: Optional unit string
            tags: Optional dict of tags
            extra_metadata: Optional dict of additional context
            **kwargs: Extra fields to override

        Returns:
            Metric: Uncommitted instance ready for session.add()
        """
        return cls(
            metric_name=metric_name,
            metric_value=value,
            metric_unit=unit,
            service_name=service,
            tags=tags or {},
            extra_metadata=extra_metadata or {},  # 🔧 Renamed field
            **kwargs
        )
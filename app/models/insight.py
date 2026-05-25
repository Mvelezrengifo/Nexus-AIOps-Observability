"""
Pydantic schemas for AI Insights.
"""

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import Field, field_validator

from app.models.common import BaseSchema


class InsightCreate(BaseSchema):
    """Schema for creating a new AI insight."""

    insight_type: str = Field(..., min_length=1, max_length=50)
    anomaly_type: str | None = Field(None, max_length=100)
    source_service: str = Field(..., min_length=1, max_length=100)
    source_event_id: str | None = Field(None, max_length=36)
    correlation_id: str | None = Field(None, max_length=36)
    title: str = Field(..., min_length=1, max_length=255)
    summary: str | None = Field(None)
    description: str = Field(..., min_length=1)
    confidence_score: Decimal = Field(default=Decimal("0.5"), ge=0, le=1)
    impact_score: Decimal | None = Field(None, ge=0, le=1)
    recommendation_level: str = Field(default="INFO")
    recommendation: str | None = None
    action_items: list[str] | None = None
    affected_resources: list[dict[str, Any]] | None = None
    related_metrics: dict[str, Any] | None = None
    model_provider: str | None = Field(None, max_length=50)
    model_name: str | None = Field(None, max_length=100)

    @field_validator("recommendation_level")
    @classmethod
    def validate_recommendation_level(cls, v: str) -> str:
        valid = ["INFO", "WARNING", "ACTION_REQUIRED", "CRITICAL"]
        if v not in valid:
            raise ValueError(f"recommendation_level must be one of: {valid}")
        return v


class InsightResponse(BaseSchema):
    """Schema for AI insight response."""

    id: int
    insight_id: str
    insight_type: str
    anomaly_type: str | None
    source_service: str
    title: str
    summary: str | None
    description: str
    confidence_score: Decimal
    impact_score: Decimal | None
    recommendation_level: str
    recommendation: str | None
    action_items: list[str] | None
    affected_resources: list[dict[str, Any]] | None
    related_metrics: dict[str, Any] | None
    model_provider: str | None
    model_name: str | None
    is_acknowledged: bool
    acknowledged_by: str | None
    acknowledged_at: datetime | None
    created_at: datetime
    updated_at: datetime


class InsightFilter(BaseSchema):
    """Schema for filtering insights."""

    insight_type: str | None = None
    source_service: str | None = None
    recommendation_level: str | None = None
    is_acknowledged: bool | None = None
    min_confidence: Decimal | None = Field(None, ge=0, le=1)
    created_after: datetime | None = None
    created_before: datetime | None = None
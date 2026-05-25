"""
Pydantic schemas for Operational Scoring.
"""

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import Field

from app.models.common import BaseSchema


class ScoringRequest(BaseSchema):
    """Schema for scoring request."""

    source_service: str = Field(..., min_length=1, max_length=100)
    event_ids: list[str] | None = Field(None, description="Specific events to score")
    time_window_minutes: int = Field(default=60, ge=1, le=1440)
    include_historical: bool = Field(default=False)
    context: dict[str, Any] | None = None


class ScoringResult(BaseSchema):
    """Schema for individual scoring result."""

    metric_name: str
    value: Decimal
    threshold: Decimal | None
    status: str  # OK, WARNING, CRITICAL
    contribution_percentage: Decimal


class ScoringResponse(BaseSchema):
    """Schema for scoring response."""

    score_id: str
    source_service: str
    overall_score: Decimal = Field(..., ge=0, le=100)
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    components: list[ScoringResult]
    recommendations: list[str] | None
    calculated_at: datetime
    time_window: dict[str, datetime]
    metadata: dict[str, Any] | None
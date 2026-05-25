"""
Pydantic schemas for Predictions.
"""

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import Field

from app.models.common import BaseSchema


class PredictionRequest(BaseSchema):
    """Schema for prediction request."""

    prediction_type: str = Field(..., min_length=1, max_length=50)
    source_service: str = Field(..., min_length=1, max_length=100)
    target_metric: str | None = Field(None, max_length=100)
    historical_data: dict[str, Any] | None = None
    time_horizon_hours: int = Field(default=24, ge=1, le=720)
    include_confidence_interval: bool = Field(default=True)
    context: dict[str, Any] | None = None


class PredictionPoint(BaseSchema):
    """Schema for a single prediction point."""

    timestamp: datetime
    predicted_value: Decimal
    confidence_lower: Decimal | None
    confidence_upper: Decimal | None


class PredictionResponse(BaseSchema):
    """Schema for prediction response."""

    prediction_id: str
    prediction_type: str
    source_service: str
    target_metric: str | None
    model_used: str
    confidence_score: Decimal
    predictions: list[PredictionPoint]
    trend: str  # INCREASING, DECREASING, STABLE
    anomaly_probability: Decimal
    insights: list[str] | None
    calculated_at: datetime
    time_horizon_hours: int
"""
Pydantic schemas for Operational Events.
"""

from datetime import datetime
from typing import Any

from pydantic import Field, field_validator

from app.models.common import BaseSchema


class EventCreate(BaseSchema):
    """Schema for creating a new operational event."""

    event_type: str = Field(..., min_length=1, max_length=100)
    event_name: str = Field(..., min_length=1, max_length=200)
    source_service: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    payload: dict[str, Any] | None = None
    severity: str = Field(default="LOW")
    correlation_id: str | None = Field(None, max_length=36)
    parent_event_id: str | None = Field(None, max_length=36)
    user_id: str | None = Field(None, max_length=36)
    actor_type: str | None = Field(None, max_length=50)
    tags: list[str] | None = None
    metadata: dict[str, Any] | None = None

    @field_validator("severity")
    @classmethod
    def validate_severity(cls, v: str) -> str:
        valid = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        if v not in valid:
            raise ValueError(f"severity must be one of: {valid}")
        return v


class EventResponse(BaseSchema):
    """Schema for operational event response."""

    id: int
    event_id: str
    event_type: str
    event_name: str
    source_service: str
    description: str | None
    payload: dict[str, Any] | None
    severity: str
    status: str
    occurred_at: datetime
    processed_at: datetime | None
    correlation_id: str | None
    parent_event_id: str | None
    user_id: str | None
    actor_type: str | None
    tags: list[str] | None
    metadata: dict[str, Any] | None
    created_at: datetime
    updated_at: datetime


class EventFilter(BaseSchema):
    """Schema for filtering events."""

    event_type: str | None = None
    source_service: str | None = None
    severity: str | None = None
    status: str | None = None
    correlation_id: str | None = None
    user_id: str | None = None
    occurred_after: datetime | None = None
    occurred_before: datetime | None = None
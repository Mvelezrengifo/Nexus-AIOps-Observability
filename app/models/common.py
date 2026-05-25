"""
Common schemas shared across the application.
"""

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints."""

    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")

    @property
    def offset(self) -> int:
        """Calculate offset for database query."""
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseSchema, Generic[T]):
    """Generic paginated response wrapper."""

    success: bool = True
    data: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def create(
            cls,
            data: list[T],
            total: int,
            page: int,
            page_size: int,
    ) -> "PaginatedResponse[T]":
        """Create paginated response with calculated total pages."""
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
        return cls(
            success=True,
            data=data,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )


class ErrorResponse(BaseSchema):
    """Standard error response."""

    success: bool = False
    error_code: str
    message: str
    details: dict[str, Any] | None = None


class SuccessResponse(BaseSchema):
    """Standard success response."""

    success: bool = True
    message: str
    data: dict[str, Any] | None = None


class HealthResponse(BaseSchema):
    """Health check response."""

    status: str
    service: str
    version: str
    environment: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    components: dict[str, str] | None = None
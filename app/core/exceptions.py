"""
Custom exceptions for the NEXUS backend.
Provides structured error handling with HTTP integration.
"""

from typing import Any


class NexusException(Exception):
    """
    Base exception for all NEXUS errors.

    Attributes:
        message: Human-readable error message
        error_code: Machine-readable error code
        status_code: HTTP status code
        details: Additional error details
    """

    def __init__(
            self,
            message: str,
            error_code: str = "INTERNAL_ERROR",
            status_code: int = 500,
            details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for API responses."""
        result = {
            "success": False,
            "error": {
                "code": self.error_code,
                "message": self.message,
            },
        }
        if self.details:
            result["error"]["details"] = self.details
        return result


class NotFoundException(NexusException):
    """Raised when a requested resource is not found."""

    def __init__(
            self,
            resource: str,
            identifier: str | int | None = None,
            details: dict[str, Any] | None = None,
    ) -> None:
        message = f"{resource} not found"
        if identifier:
            message = f"{resource} with id '{identifier}' not found"

        super().__init__(
            message=message,
            error_code="NOT_FOUND",
            status_code=404,
            details=details,
        )


class ValidationException(NexusException):
    """Raised when input validation fails."""

    def __init__(
            self,
            message: str = "Validation error",
            details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422,
            details=details,
        )


class AuthenticationException(NexusException):
    """Raised when authentication fails."""

    def __init__(
            self,
            message: str = "Authentication failed",
            details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=401,
            details=details,
        )


class AuthorizationException(NexusException):
    """Raised when user lacks required permissions."""

    def __init__(
            self,
            message: str = "Insufficient permissions",
            details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=403,
            details=details,
        )


class ServiceException(NexusException):
    """Raised when an external service fails."""

    def __init__(
            self,
            service: str,
            message: str = "Service unavailable",
            details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=f"{service}: {message}",
            error_code="SERVICE_ERROR",
            status_code=503,
            details=details,
        )


class AIServiceException(NexusException):
    """Raised when AI service (Groq, OpenAI) fails."""

    def __init__(
            self,
            provider: str,
            message: str = "AI service error",
            details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=f"{provider}: {message}",
            error_code="AI_SERVICE_ERROR",
            status_code=500,
            details=details,
        )


class DatabaseException(NexusException):
    """Raised when a database operation fails."""

    def __init__(
            self,
            operation: str,
            message: str = "Database operation failed",
            details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=f"{operation}: {message}",
            error_code="DATABASE_ERROR",
            status_code=500,
            details=details,
        )
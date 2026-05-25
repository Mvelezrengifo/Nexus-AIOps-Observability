"""
Structured logging configuration using structlog.
Provides JSON logging for production and colored output for development.
"""

import logging
import sys
from typing import Any

import structlog
from structlog.types import Processor

from app.config import settings


def setup_logging() -> None:
    """
    Configure structured logging for the application.

    In development: colored, human-readable output.
    In production: JSON format for observability platforms.
    """

    # Shared processors for all environments
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.is_production:
        # Production: JSON logging for CloudWatch, Datadog, etc.
        processors: list[Processor] = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    else:
        # Development: colored, human-readable
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.log_level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard logging to use structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.getLevelName(settings.log_level),
    )


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """
    Get a configured structlog logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


class LoggerMixin:
    """Mixin to add logging capability to classes."""

    _logger: structlog.stdlib.BoundLogger | None = None

    @property
    def logger(self) -> structlog.stdlib.BoundLogger:
        """Get or create logger for this class."""
        if self._logger is None:
            self._logger = get_logger(self.__class__.__module__)
        return self._logger


def log_context(**kwargs: Any) -> None:
    """
    Add context variables to all subsequent log messages in this context.

    Usage:
        log_context(user_id="123", request_id="abc")
        logger.info("Processing request")  # Will include user_id and request_id
    """
    structlog.contextvars.bind_contextvars(**kwargs)


def clear_log_context() -> None:
    """Clear all context variables from logging."""
    structlog.contextvars.clear_contextvars()
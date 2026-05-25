"""
Audit Trail model - tracks all system actions for compliance.
"""

from enum import Enum
from typing import Any

from sqlalchemy import String, Text, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AuditAction(str, Enum):
    """Types of auditable actions."""
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    EXPORT = "EXPORT"
    IMPORT = "IMPORT"
    CONFIG_CHANGE = "CONFIG_CHANGE"


class AuditTrail(Base):
    """
    Audit Trail table.

    Records all significant actions for compliance and security.
    """

    __tablename__ = "audit_trails"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Audit identification
    audit_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
    )

    # Action details
    action: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)

    # Actor information
    user_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    user_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    actor_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Request context
    request_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    session_id: Mapped[str | None] = mapped_column(String(36), nullable=True)

    # Changes
    old_values: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    new_values: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    changed_fields: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    # Additional context
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # Status
    success: Mapped[bool] = mapped_column(default=True, index=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Indexes
    __table_args__ = (
        Index("ix_audit_trails_user_action", "user_id", "action"),
        Index("ix_audit_trails_resource", "resource_type", "resource_id"),
        Index("ix_audit_trails_created", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<AuditTrail(id={self.id}, action={self.action}, resource={self.resource_type})>"
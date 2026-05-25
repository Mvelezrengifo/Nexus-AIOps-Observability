"""
Database model for user accounts and authentication.
SQLAlchemy ORM model - DO NOT mix with Pydantic schemas.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Integer,
    func,
    Index,
    event,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.core.security import hash_password, verify_password


class User(Base):
    """
    ORM model for user accounts.

    Supports RBAC, audit trails, and secure credential storage.
    """

    __tablename__ = "users"

    # ===== PRIMARY KEY =====
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # ===== AUTHENTICATION =====
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)

    # ===== PROFILE =====
    full_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)

    # 🔧 FIX DEFINITIVO: permissions como JSONB (NO usar Mapped[list[str]])
    # SQLAlchemy no resuelve list[str] automáticamente en Windows + Python 3.14
    permissions = Column(JSONB, default=list, nullable=True)

    # ===== RBAC =====
    role = Column(String(50), nullable=False, default="analyst", index=True)

    # ===== AUDIT & TEMPORAL =====
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ===== INDEXES =====
    __table_args__ = (
        Index("ix_users_email_active", "email", "is_active"),
        Index("ix_users_role_created", "role", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"

    # ===== SECURITY METHODS =====

    def set_password(self, plain_password: str) -> None:
        """Hash and store password securely."""
        self.hashed_password = hash_password(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        """Verify password against stored hash."""
        return verify_password(plain_password, self.hashed_password)

    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission."""
        if not self.permissions:
            return False
        return permission in self.permissions

    def has_role(self, role: str) -> bool:
        """Check if user has a specific role (with hierarchy)."""
        role_hierarchy = {
            "admin": ["admin", "analyst", "viewer"],
            "analyst": ["analyst", "viewer"],
            "viewer": ["viewer"],
        }
        return role in role_hierarchy.get(self.role, [])

    def record_login(self, success: bool) -> None:
        """Update login tracking fields."""
        if success:
            self.last_login_at = datetime.utcnow()
            self.failed_login_attempts = 0
            self.locked_until = None
        else:
            self.failed_login_attempts += 1
            if self.failed_login_attempts >= 5 and not self.locked_until:
                from datetime import timedelta
                self.locked_until = datetime.utcnow() + timedelta(minutes=30)

    def is_locked(self) -> bool:
        """Check if account is temporarily locked."""
        if not self.locked_until:
            return False
        return datetime.utcnow() < self.locked_until

    # ===== SERIALIZATION =====

    def to_dict(self, include_sensitive: bool = False) -> dict:
        """Convert user to dictionary for API responses."""
        data = {
            "id": str(self.id),
            "email": self.email,
            "full_name": self.full_name,
            "avatar_url": self.avatar_url,
            "role": self.role,
            "permissions": self.permissions or [],
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
        }
        if include_sensitive:
            data["hashed_password"] = self.hashed_password
        return data

    # ===== FACTORY METHODS =====

    @classmethod
    def create_admin(cls, email: str, password: str, full_name: Optional[str] = None) -> "User":
        """Create an admin user."""
        user = cls(
            email=email,
            full_name=full_name or "Admin User",
            role="admin",
            permissions=["*"],
            is_active=True,
            is_verified=True,
        )
        user.set_password(password)
        return user

    @classmethod
    def create_analyst(cls, email: str, password: str, permissions: Optional[list] = None) -> "User":
        """Create an analyst user."""
        user = cls(
            email=email,
            role="analyst",
            permissions=permissions or ["read:metrics", "read:insights"],
            is_active=True,
            is_verified=False,
        )
        user.set_password(password)
        return user


# ===== EVENT LISTENERS =====

@event.listens_for(User, "before_insert")
def receive_before_insert(mapper, connection, target):
    """Auto-hash password on creation if not already hashed."""
    if target.hashed_password and not target.hashed_password.startswith("$2b$"):
        target.hashed_password = hash_password(target.hashed_password)
"""
Pydantic schemas for user-related API requests/responses.
These are DTOs (Data Transfer Objects) for validation and serialization.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


# ===== SCHEMAS PARA REQUESTS =====

class UserCreate(BaseModel):
    """Schema for creating a new user (signup)."""
    email: EmailStr = Field(..., description="User email address", max_length=255)
    password: str = Field(..., min_length=8, description="Password (min 8 chars)")
    full_name: Optional[str] = Field(None, max_length=100)
    role: Optional[str] = Field("analyst", pattern="^(admin|analyst|viewer)$")
    permissions: Optional[List[str]] = Field(default_factory=list)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v) or not any(c.islower() for c in v):
            raise ValueError("Password must contain upper and lowercase letters")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")
    remember_me: Optional[bool] = Field(False)


class UserUpdate(BaseModel):
    """Schema for updating user profile (partial updates)."""
    full_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)
    role: Optional[str] = Field(None, pattern="^(admin|analyst|viewer)$")
    permissions: Optional[List[str]] = None
    is_active: Optional[bool] = None

    # Password change is handled separately for security
    new_password: Optional[str] = Field(None, min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


# ===== SCHEMAS PARA RESPONSES =====

class UserResponse(BaseModel):
    """Schema for user data in API responses (no sensitive fields)."""
    id: UUID
    email: EmailStr
    full_name: Optional[str]
    avatar_url: Optional[str]
    role: str
    permissions: List[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login_at: Optional[datetime]

    class Config:
        from_attributes = True  # SQLAlchemy 2.0 compatibility


class UserPublic(BaseModel):
    """Minimal user info for public contexts (e.g., audit logs)."""
    id: UUID
    email: EmailStr
    full_name: Optional[str]
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(3600, description="Token validity in seconds")
    refresh_token: Optional[str] = None


class TokenPayload(BaseModel):
    """Decoded JWT payload structure (for internal use)."""
    sub: UUID  # user id
    email: EmailStr
    role: str
    permissions: List[str]
    exp: datetime
    iat: datetime

    class Config:
        from_attributes = True


# ===== SCHEMAS PARA AUTH FLOWS =====

class PasswordChangeRequest(BaseModel):
    """Schema for password change (requires current password)."""
    current_password: str = Field(..., description="Current password for verification")
    new_password: str = Field(..., min_length=8, description="New password")

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v) or not any(c.islower() for c in v):
            raise ValueError("Password must contain upper and lowercase letters")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class PasswordResetRequest(BaseModel):
    """Schema for requesting password reset email."""
    email: EmailStr = Field(..., description="Email to send reset link")


class PasswordResetConfirm(BaseModel):
    """Schema for confirming password reset with token."""
    token: str = Field(..., description="Reset token from email")
    new_password: str = Field(..., min_length=8, description="New password")

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


# ===== UTILS =====

def sanitize_user_output(user_data: dict) -> dict:
    """
    Remove sensitive fields from user dict before sending to client.

    Args:
        user_data: Dict from SQLAlchemy model or DB query

    Returns:
        dict: Sanitized for API response
    """
    sensitive_fields = {"hashed_password", "password", "reset_token", "mfa_secret"}
    return {k: v for k, v in user_data.items() if k not in sensitive_fields}
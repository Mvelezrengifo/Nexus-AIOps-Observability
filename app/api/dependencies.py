"""
Dependency injection for API endpoints.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.security import decode_access_token
from app.core.exceptions import AuthenticationException
from app.repositories.user_repository import UserRepository

# Database session dependency
DBSession = Annotated[AsyncSession, Depends(get_db)]

# Security scheme
security = HTTPBearer(auto_error=False)


async def get_current_user(
        db: DBSession,
        credentials: Annotated[
            HTTPAuthorizationCredentials | None,
            Depends(security),
        ] = None,
) -> dict | None:
    """
    Extract and validate current user from JWT token.

    Returns user info if authenticated, None otherwise.
    """
    if credentials is None:
        return None

    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise AuthenticationException("Invalid or expired token")

    user_repo = UserRepository(db)
    user = await user_repo.get_by_user_id(payload.get("sub"))

    if user is None or not user.is_active:
        raise AuthenticationException("User not found or inactive")

    return {
        "user_id": user.user_id,
        "email": user.email,
        "role": user.role,
    }


async def require_auth(
        user: Annotated[dict | None, Depends(get_current_user)],
) -> dict:
    """
    Require authenticated user.
    Raises 401 if not authenticated.
    """
    if user is None:
        raise AuthenticationException("Authentication required")
    return user


# Type aliases for cleaner function signatures
CurrentUser = Annotated[dict, Depends(require_auth)]
OptionalUser = Annotated[dict | None, Depends(get_current_user)]
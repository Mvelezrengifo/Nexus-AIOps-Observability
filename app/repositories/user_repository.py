"""
Repository for Users.
"""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for user accounts."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_user_id(self, user_id: str) -> User | None:
        """Get user by its unique ID."""
        return await self.get_by_field("user_id", user_id)

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email address."""
        return await self.get_by_field("email", email)

    async def get_active_users(
            self,
            skip: int = 0,
            limit: int = 100,
    ) -> list[User]:
        """Get all active users."""
        result = await self.session.execute(
            select(User)
            .where(User.is_active == True)
            .order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_role(
            self,
            role: str,
            skip: int = 0,
            limit: int = 100,
    ) -> list[User]:
        """Get users by role."""
        result = await self.session.execute(
            select(User)
            .where(User.role == role)
            .where(User.is_active == True)
            .order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def authenticate(self, email: str, password_hash: str) -> User | None:
        """Verify user credentials (password check done in service)."""
        user = await self.get_by_email(email)

        if user is None or not user.is_active:
            return None

        return user

    async def update_last_login(
            self,
            user_id: str,
            ip_address: str | None = None,
    ) -> User | None:
        """Update last login timestamp."""
        user = await self.get_by_user_id(user_id)

        if user is None:
            return None

        from datetime import datetime

        return await self.update(
            user.id,
            {
                "last_login_at": datetime.utcnow().isoformat(),
                "last_login_ip": ip_address,
                "failed_login_attempts": 0,
            },
        )

    async def increment_failed_login(self, email: str) -> None:
        """Increment failed login attempts."""
        user = await self.get_by_email(email)

        if user:
            await self.update(
                user.id,
                {"failed_login_attempts": user.failed_login_attempts + 1},
            )

    async def create_user(
            self,
            email: str,
            password_hash: str,
            role: str = "VIEWER",
            **kwargs: Any,
    ) -> User:
        """Create a new user."""
        data = {
            "user_id": self._generate_uuid(),
            "email": email,
            "password_hash": password_hash,
            "role": role,
            **kwargs,
        }

        return await self.create(data)
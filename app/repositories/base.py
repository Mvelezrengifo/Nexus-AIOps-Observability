"""
Base repository with common CRUD operations.
"""

from typing import Any, Generic, TypeVar
from uuid import uuid4

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.base import Base

logger = get_logger(__name__)

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository with common database operations.

    Provides CRUD operations for any SQLAlchemy model.
    """

    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        """
        Initialize repository.

        Args:
            model: SQLAlchemy model class
            session: Async database session
        """
        self.model = model
        self.session = session

    async def create(self, data: dict[str, Any]) -> ModelType:
        """
        Create a new record.

        Args:
            data: Dictionary with model field values

        Returns:
            Created model instance
        """
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)

        logger.debug(
            f"Created {self.model.__name__}",
            id=instance.id,
        )

        return instance

    async def get_by_id(self, id: int) -> ModelType | None:
        """
        Get a record by its primary key ID.

        Args:
            id: Primary key value

        Returns:
            Model instance or None
        """
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_field(self, field: str, value: Any) -> ModelType | None:
        """
        Get a record by a specific field value.

        Args:
            field: Field name
            value: Field value

        Returns:
            Model instance or None
        """
        column = getattr(self.model, field)
        result = await self.session.execute(
            select(self.model).where(column == value)
        )
        return result.scalar_one_or_none()

    async def get_all(
            self,
            skip: int = 0,
            limit: int = 100,
    ) -> list[ModelType]:
        """
        Get all records with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum records to return

        Returns:
            List of model instances
        """
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def update(
            self,
            id: int,
            data: dict[str, Any],
    ) -> ModelType | None:
        """
        Update a record by ID.

        Args:
            id: Primary key value
            data: Fields to update

        Returns:
            Updated model instance or None
        """
        instance = await self.get_by_id(id)

        if instance is None:
            return None

        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        await self.session.flush()
        await self.session.refresh(instance)

        logger.debug(
            f"Updated {self.model.__name__}",
            id=instance.id,
        )

        return instance

    async def delete(self, id: int) -> bool:
        """
        Delete a record by ID.

        Args:
            id: Primary key value

        Returns:
            True if deleted, False if not found
        """
        instance = await self.get_by_id(id)

        if instance is None:
            return False

        await self.session.delete(instance)
        await self.session.flush()

        logger.debug(
            f"Deleted {self.model.__name__}",
            id=id,
        )

        return True

    async def count(self) -> int:
        """
        Count total records.

        Returns:
            Total number of records
        """
        result = await self.session.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar_one()

    async def exists(self, id: int) -> bool:
        """
        Check if a record exists.

        Args:
            id: Primary key value

        Returns:
            True if exists, False otherwise
        """
        result = await self.session.execute(
            select(func.count()).where(self.model.id == id)
        )
        return result.scalar_one() > 0

    def _generate_uuid(self) -> str:
        """Generate a UUID string."""
        return str(uuid4())
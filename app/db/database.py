"""
Database connection and session management using SQLAlchemy async.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import AsyncContextManager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool

from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# =====================================================================
# PARCHE DE INFRAESTRUCTURA: Forzar psycopg para Python 3.14 + Windows
# =====================================================================
raw_url = str(settings.database_url)

if "asyncpg" in raw_url:
    fixed_url = raw_url.replace("asyncpg", "psycopg")
elif "postgresql://" in raw_url:
    fixed_url = raw_url.replace("postgresql://", "postgresql+psycopg://")
else:
    fixed_url = raw_url

# Configuramos los argumentos del pool según el entorno
# Si es producción (NullPool), no podemos pasar pool_size ni max_overflow
pool_args = {}
if settings.is_production:
    pool_args["poolclass"] = NullPool
else:
    pool_args["pool_size"] = 5
    pool_args["max_overflow"] = 10

# Create async engine con la URL corregida a la fuerza
engine: AsyncEngine = create_async_engine(
    fixed_url,
    echo=settings.debug,  # Log SQL queries in debug mode
    pool_pre_ping=True,  # Verify connections before using
    **pool_args
)
# =====================================================================

# Session factory
async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency injection for database sessions.
    Use with FastAPI Depends().

    Yields:
        AsyncSession: Database session

    Usage:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for database sessions.
    Use outside of FastAPI dependency injection.

    Yields:
        AsyncSession: Database session

    Usage:
        async with get_db_context() as db:
            result = await db.execute(query)
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize database - create all tables.
    Called on application startup if needed.
    """
    from app.db.base import Base

    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database tables created")


async def close_db() -> None:
    """
    Close database connections.
    Called on application shutdown.
    """
    await engine.dispose()
    logger.info("Database connections closed")
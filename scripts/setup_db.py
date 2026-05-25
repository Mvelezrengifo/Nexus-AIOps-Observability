"""
Script to initialize database tables.
Run: python scripts/setup_db.py
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.database import engine, init_db
from app.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


async def main():
    """Initialize database."""
    logger.info("Setting up database...")

    try:
        await init_db()
        logger.info("Database setup complete!")
    except Exception as e:
        logger.error("Database setup failed", error=str(e))
        sys.exit(1)
    finally:
        from app.db.database import close_db
        await close_db()


if __name__ == "__main__":
    asyncio.run(main())
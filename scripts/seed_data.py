"""
Script to seed database with sample data.
Run: python scripts/seed_data.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.database import async_session_factory
from app.repositories.event_repository import EventRepository
from app.repositories.insight_repository import InsightRepository
from app.repositories.metric_repository import MetricRepository
from app.core.logging import setup_logging, get_logger
from decimal import Decimal

setup_logging()
logger = get_logger(__name__)


async def seed_events(session):
    """Seed sample events."""
    repo = EventRepository(session)

    events_data = [
        {
            "event_type": "DEPLOYMENT",
            "event_name": "Service deployed",
            "source_service": "nexus-api",
            "severity": "LOW",
            "description": "Successfully deployed version 1.0.0",
        },
        {
            "event_type": "ERROR",
            "event_name": "Database connection failed",
            "source_service": "nexus-api",
            "severity": "HIGH",
            "description": "Connection timeout to PostgreSQL",
        },
        {
            "event_type": "WARNING",
            "event_name": "High CPU usage",
            "source_service": "nexus-worker",
            "severity": "MEDIUM",
            "description": "CPU usage above 80%",
        },
    ]

    for data in events_data:
        await repo.create_event(**data)

    logger.info(f"Seeded {len(events_data)} events")


async def seed_insights(session):
    """Seed sample insights."""
    repo = InsightRepository(session)

    insights_data = [
        {
            "insight_type": "ANOMALY_DETECTION",
            "source_service": "nexus-api",
            "title": "Unusual traffic pattern detected",
            "description": "Request rate increased by 300%",
            "confidence_score": Decimal("0.85"),
            "recommendation_level": "WARNING",
        },
        {
            "insight_type": "TREND_ANALYSIS",
            "source_service": "nexus-worker",
            "title": "Memory usage trend",
            "description": "Memory consumption steadily increasing",
            "confidence_score": Decimal("0.72"),
            "recommendation_level": "INFO",
        },
    ]

    for data in insights_data:
        await repo.create_insight(**data)

    logger.info(f"Seeded {len(insights_data)} insights")


async def seed_metrics(session):
    """Seed sample metrics."""
    repo = MetricRepository(session)

    metrics_data = [
        {
            "metric_name": "cpu_usage",
            "metric_type": "GAUGE",
            "source_service": "nexus-api",
            "value": Decimal("45.5"),
            "unit": "percent",
        },
        {
            "metric_name": "memory_usage",
            "metric_type": "GAUGE",
            "source_service": "nexus-api",
            "value": Decimal("1024.0"),
            "unit": "MB",
        },
        {
            "metric_name": "request_count",
            "metric_type": "COUNTER",
            "source_service": "nexus-api",
            "value": Decimal("1500"),
            "unit": "requests",
        },
    ]

    for data in metrics_data:
        await repo.create_metric(**data)

    logger.info(f"Seeded {len(metrics_data)} metrics")


async def main():
    """Seed all data."""
    logger.info("Starting database seeding...")

    async with async_session_factory() as session:
        await seed_events(session)
        await seed_insights(session)
        await seed_metrics(session)
        await session.commit()

    logger.info("Database seeding complete!")


if __name__ == "__main__":
    asyncio.run(main())
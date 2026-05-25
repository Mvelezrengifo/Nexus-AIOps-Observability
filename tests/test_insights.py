"""
Tests for AI Insights endpoints.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_list_insights(client: AsyncClient):
    """Test listing insights."""
    response = await client.get("/api/v1/insights")

    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert "data" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_create_insight_unauthorized(client: AsyncClient):
    """Test creating insight without auth."""
    response = await client.post(
        "/api/v1/insights",
        json={
            "insight_type": "ANOMALY_DETECTION",
            "source_service": "test-service",
            "title": "Test Insight",
            "description": "Test description",
        },
    )

    assert response.status_code == 401
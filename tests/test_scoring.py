"""
Tests for Scoring endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_quick_score(client: AsyncClient):
    """Test quick score endpoint."""
    response = await client.get("/api/v1/scoring/quick/test-service")

    assert response.status_code == 200
    data = response.json()

    assert "service" in data
    assert "score" in data
    assert "risk_level" in data


@pytest.mark.asyncio
async def test_score_calculation(client: AsyncClient):
    """Test score calculation."""
    response = await client.post(
        "/api/v1/scoring",
        json={
            "source_service": "test-service",
            "time_window_minutes": 60,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert "score_id" in data
    assert "overall_score" in data
    assert "risk_level" in data
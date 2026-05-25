"""
Tests for Events endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_events(client: AsyncClient):
    """Test listing events."""
    response = await client.get("/api/v1/events")

    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert "data" in data


@pytest.mark.asyncio
async def test_event_stats(client: AsyncClient):
    """Test event statistics."""
    response = await client.get("/api/v1/events/stats/summary")

    assert response.status_code == 200
    data = response.json()

    assert "total_events" in data
    assert "by_severity" in data
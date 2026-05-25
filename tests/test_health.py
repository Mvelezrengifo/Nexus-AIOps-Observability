"""
Tests for health check endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test basic health endpoint."""
    response = await client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_readiness_check(client: AsyncClient):
    """Test readiness endpoint."""
    response = await client.get("/health/ready")

    assert response.status_code == 200
    data = response.json()

    assert data["ready"] is True
    assert "checks" in data


@pytest.mark.asyncio
async def test_liveness_check(client: AsyncClient):
    """Test liveness endpoint."""
    response = await client.get("/health/live")

    assert response.status_code == 200
    data = response.json()

    assert data["alive"] is True
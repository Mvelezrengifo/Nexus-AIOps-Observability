"""
API endpoints module.
"""

from fastapi import APIRouter

from app.api.endpoints import health, insights, events, scoring, predict

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(insights.router, prefix="/insights", tags=["Insights"])
api_router.include_router(events.router, prefix="/events", tags=["Events"])
api_router.include_router(scoring.router, prefix="/scoring", tags=["Scoring"])
api_router.include_router(predict.router, prefix="/predict", tags=["Predictions"])
"""
NEXUS Backend - Main FastAPI Application.
Entry point for the API server.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from app.config import settings
from app.core.logging import setup_logging, get_logger
from app.core.middleware import (
    RequestIDMiddleware,
    TimingMiddleware,
    ExceptionHandlerMiddleware,
)

# Setup logging before anything else
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler."""
    logger.info(
        "Starting NEXUS Backend",
        app_name=settings.app_name,
        environment=settings.app_env,
        version=settings.app_version,
    )

    app.state.settings = settings

    from app.clients.event_bus_client import get_event_bus

    app.state.event_bus = get_event_bus()

    yield

    logger.info("Shutting down NEXUS Backend")

    event_bus = getattr(app.state, "event_bus", None)
    if event_bus:
        await event_bus.close()


app = FastAPI(
    title=settings.app_name,
    description="""
    NEXUS Operational Intelligence Platform API.

    Enterprise-grade backend for:
    - Operational monitoring
    - AI-powered insights
    - Event correlation
    - Predictive analytics
    - Distributed observability
    """,
    version=settings.app_version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
    lifespan=lifespan,
)

app.add_middleware(ExceptionHandlerMiddleware)
app.add_middleware(TimingMiddleware)
app.add_middleware(RequestIDMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """Basic health check endpoint."""
    logger.debug("Health check requested")
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@app.get("/", tags=["Root"])
async def root() -> dict:
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs" if settings.debug else "disabled",
        "health": "/health",
        "graphql": "/graphql",
    }


from app.api.endpoints import api_router
from app.api.endpoints.health import router as health_router
from app.api.endpoints.events import router as events_router
from app.api.endpoints.insights import router as insights_router

app.include_router(api_router, prefix=settings.api_prefix)
app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(events_router, prefix=settings.api_prefix)
app.include_router(insights_router, prefix=settings.api_prefix)

from app.api.graphql.schema import schema

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_development,
        log_level=settings.log_level.lower(),
    )
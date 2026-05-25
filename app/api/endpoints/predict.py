"""
Predictions endpoints.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.logging import get_logger
from app.models.prediction import PredictionRequest, PredictionResponse
from app.services.prediction_service import PredictionService
from app.api.dependencies import CurrentUser, OptionalUser

router = APIRouter()
logger = get_logger(__name__)


@router.post("", response_model=PredictionResponse)
async def create_prediction(
        request: PredictionRequest,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: OptionalUser = None,
) -> PredictionResponse:
    """
    Generate an operational prediction.

    Uses AI to forecast future states based on patterns.
    """
    logger.info(
        "Creating prediction",
        type=request.prediction_type,
        service=request.source_service,
        horizon=request.time_horizon_hours,
    )

    service = PredictionService(db)

    result = await service.predict(
        prediction_type=request.prediction_type,
        source_service=request.source_service,
        target_metric=request.target_metric,
        time_horizon_hours=request.time_horizon_hours,
        context=request.context,
    )

    return PredictionResponse(**result)


@router.post("/resource-usage")
async def predict_resource(
        source_service: str = Body(..., embed=True),
        resource_type: str = Body(..., embed=True),
        time_horizon_hours: int = Body(24, embed=True),
        db: Annotated[AsyncSession, Depends(get_db)] = None,
        current_user: OptionalUser = None,
) -> dict:
    """
    Predict resource usage for a service.

    Forecasts CPU, memory, or other resource consumption.
    """
    logger.info(
        "Predicting resource usage",
        service=source_service,
        resource=resource_type,
    )

    service = PredictionService(db)

    result = await service.predict_resource_usage(
        source_service=source_service,
        resource_type=resource_type,
        time_horizon_hours=time_horizon_hours,
    )

    return result


@router.post("/incident-risk")
async def predict_incident(
        source_service: str = Body(..., embed=True),
        time_horizon_hours: int = Body(24, embed=True),
        db: Annotated[AsyncSession, Depends(get_db)] = None,
        current_user: OptionalUser = None,
) -> dict:
    """
    Predict incident risk for a service.

    Estimates probability of incidents occurring.
    """
    logger.info(
        "Predicting incident risk",
        service=source_service,
        horizon=time_horizon_hours,
    )

    service = PredictionService(db)

    result = await service.predict_incident_risk(
        source_service=source_service,
        time_horizon_hours=time_horizon_hours,
    )

    return result


@router.get("/types")
async def list_prediction_types(
        current_user: OptionalUser = None,
) -> dict:
    """
    List available prediction types.
    """
    return {
        "prediction_types": [
            {
                "name": "RESOURCE_USAGE",
                "description": "Predict CPU, memory, and resource consumption",
            },
            {
                "name": "INCIDENT_RISK",
                "description": "Predict probability of incidents",
            },
            {
                "name": "TREND_ANALYSIS",
                "description": "Analyze metric trends over time",
            },
            {
                "name": "ANOMALY_FORECAST",
                "description": "Predict potential anomalies",
            },
            {
                "name": "CAPACITY_PLANNING",
                "description": "Forecast capacity requirements",
            },
        ]
    }
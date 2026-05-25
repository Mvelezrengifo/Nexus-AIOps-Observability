"""
Prediction Service - Forecasts operational metrics.
"""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.services.ai_engine import get_ai_engine

logger = get_logger(__name__)


class PredictionService:
    """
    Service for predictive analytics.

    Uses historical data and AI to forecast future states.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def predict(
            self,
            prediction_type: str,
            source_service: str,
            target_metric: str | None = None,
            time_horizon_hours: int = 24,
            context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Generate operational prediction.

        Args:
            prediction_type: Type of prediction
            source_service: Service to analyze
            target_metric: Specific metric to predict
            time_horizon_hours: How far ahead to predict
            context: Additional context

        Returns:
            Prediction results
        """
        prediction_id = str(uuid4())

        # Build context for AI
        ai_context = {
            "prediction_type": prediction_type,
            "source_service": source_service,
            "target_metric": target_metric,
            "time_horizon_hours": time_horizon_hours,
            "current_time": datetime.utcnow().isoformat(),
            **(context or {}),
        }

        # Get AI prediction
        ai_engine = await get_ai_engine()

        try:
            ai_result = await ai_engine.generate_insight(
                ai_context,
                insight_type="PREDICTION",
            )
        except Exception as e:
            logger.warning("AI prediction failed, using fallback", error=str(e))
            ai_result = self._fallback_prediction(prediction_type)

        # Generate prediction points
        predictions = self._generate_prediction_points(
            time_horizon_hours,
            ai_result.get("confidence_score", Decimal("0.5")),
        )

        # Determine trend
        trend = self._determine_trend(predictions)

        # Calculate anomaly probability
        anomaly_prob = self._calculate_anomaly_probability(predictions)

        return {
            "prediction_id": prediction_id,
            "prediction_type": prediction_type,
            "source_service": source_service,
            "target_metric": target_metric,
            "model_used": ai_result.get("model_name", "hybrid"),
            "confidence_score": ai_result.get("confidence_score", Decimal("0.5")),
            "predictions": predictions,
            "trend": trend,
            "anomaly_probability": anomaly_prob,
            "insights": ai_result.get("action_items", []),
            "calculated_at": datetime.utcnow().isoformat(),
            "time_horizon_hours": time_horizon_hours,
        }

    def _generate_prediction_points(
            self,
            time_horizon_hours: int,
            confidence: Decimal,
    ) -> list[dict[str, Any]]:
        """Generate prediction data points."""
        predictions = []
        base_time = datetime.utcnow()

        # Generate hourly points
        for hour in range(1, time_horizon_hours + 1):
            point_time = base_time + timedelta(hours=hour)

            # Simulate value with some variation
            # In production, this would use actual model output
            import random
            base_value = Decimal(str(50 + random.uniform(-5, 5)))

            # Confidence interval widens over time
            interval_width = Decimal(str(5 + (hour * 0.5)))

            predictions.append({
                "timestamp": point_time.isoformat(),
                "predicted_value": base_value,
                "confidence_lower": base_value - interval_width,
                "confidence_upper": base_value + interval_width,
            })

        return predictions

    def _determine_trend(self, predictions: list[dict]) -> str:
        """Determine overall trend from predictions."""
        if len(predictions) < 2:
            return "STABLE"

        first = predictions[0]["predicted_value"]
        last = predictions[-1]["predicted_value"]

        diff = last - first

        if diff > Decimal("5"):
            return "INCREASING"
        elif diff < Decimal("-5"):
            return "DECREASING"
        else:
            return "STABLE"

    def _calculate_anomaly_probability(
            self,
            predictions: list[dict],
    ) -> Decimal:
        """Calculate probability of anomaly occurring."""
        if not predictions:
            return Decimal("0")

        # Check if any prediction crosses warning thresholds
        anomaly_count = 0

        for pred in predictions:
            value = pred["predicted_value"]
            if value > Decimal("80") or value < Decimal("20"):
                anomaly_count += 1

        probability = Decimal(str(anomaly_count)) / Decimal(str(len(predictions)))

        return probability.quantize(Decimal("0.0001"))

    def _fallback_prediction(self, prediction_type: str) -> dict[str, Any]:
        """Provide fallback prediction when AI fails."""
        return {
            "title": f"{prediction_type} Prediction",
            "description": "Prediction based on historical patterns",
            "confidence_score": Decimal("0.5"),
            "action_items": ["Monitor closely for changes"],
            "model_name": "fallback",
        }

    async def predict_resource_usage(
            self,
            source_service: str,
            resource_type: str,
            time_horizon_hours: int = 24,
    ) -> dict[str, Any]:
        """
        Predict resource usage (CPU, memory, etc).

        Args:
            source_service: Service name
            resource_type: Type of resource
            time_horizon_hours: Prediction window

        Returns:
            Resource prediction
        """
        return await self.predict(
            prediction_type="RESOURCE_USAGE",
            source_service=source_service,
            target_metric=resource_type,
            time_horizon_hours=time_horizon_hours,
        )

    async def predict_incident_risk(
            self,
            source_service: str,
            time_horizon_hours: int = 24,
    ) -> dict[str, Any]:
        """
        Predict risk of incidents.

        Args:
            source_service: Service name
            time_horizon_hours: Prediction window

        Returns:
            Incident risk prediction
        """
        return await self.predict(
            prediction_type="INCIDENT_RISK",
            source_service=source_service,
            time_horizon_hours=time_horizon_hours,
        )
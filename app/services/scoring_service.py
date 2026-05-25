"""
Scoring Service - Calculates operational risk scores.
"""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.repositories.event_repository import EventRepository
from app.repositories.metric_repository import MetricRepository
from app.repositories.anomaly_repository import AnomalyRepository

logger = get_logger(__name__)


class ScoringService:
    """
    Service for calculating operational scores.

    Provides risk assessment and health scores for services.
    """

    # Weights for different factors
    SEVERITY_WEIGHTS = {
        "LOW": Decimal("0.1"),
        "MEDIUM": Decimal("0.3"),
        "HIGH": Decimal("0.6"),
        "CRITICAL": Decimal("1.0"),
    }

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.event_repo = EventRepository(session)
        self.metric_repo = MetricRepository(session)
        self.anomaly_repo = AnomalyRepository(session)

    async def calculate_score(
            self,
            source_service: str,
            time_window_minutes: int = 60,
    ) -> dict[str, Any]:
        """
        Calculate operational score for a service.

        Args:
            source_service: Service to score
            time_window_minutes: Time window for analysis

        Returns:
            Score with breakdown
        """
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=time_window_minutes)

        # Get events in window
        events = await self.event_repo.get_by_time_range(
            start_time=start_time,
            end_time=end_time,
            limit=500,
        )

        service_events = [
            e for e in events if e.source_service == source_service
        ]

        # Get open anomalies
        anomalies = await self.anomaly_repo.get_by_source_service(
            source_service, limit=100
        )
        open_anomalies = [a for a in anomalies if a.status != "RESOLVED"]

        # Calculate components
        event_score = self._calculate_event_score(service_events)
        anomaly_score = self._calculate_anomaly_score(open_anomalies)

        # Combined score (weighted average)
        overall_score = (event_score * Decimal("0.6")) + (anomaly_score * Decimal("0.4"))

        # Determine risk level
        risk_level = self._determine_risk_level(overall_score)

        return {
            "score_id": str(uuid4()),
            "source_service": source_service,
            "overall_score": overall_score,
            "risk_level": risk_level,
            "components": [
                {
                    "metric_name": "event_health",
                    "value": event_score,
                    "threshold": Decimal("50"),
                    "status": "OK" if event_score >= 50 else "WARNING",
                    "contribution_percentage": Decimal("60"),
                },
                {
                    "metric_name": "anomaly_health",
                    "value": anomaly_score,
                    "threshold": Decimal("50"),
                    "status": "OK" if anomaly_score >= 50 else "WARNING",
                    "contribution_percentage": Decimal("40"),
                },
            ],
            "recommendations": self._generate_recommendations(
                overall_score, service_events, open_anomalies
            ),
            "calculated_at": datetime.utcnow().isoformat(),
            "time_window": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
            },
        }

    def _calculate_event_score(self, events: list[Any]) -> Decimal:
        """Calculate score based on events (higher = better)."""
        if not events:
            return Decimal("100")  # No events = healthy

        # Count by severity
        severity_counts: dict[str, int] = {}
        for event in events:
            sev = event.severity
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        # Calculate penalty
        penalty = Decimal("0")
        for severity, count in severity_counts.items():
            weight = self.SEVERITY_WEIGHTS.get(severity, Decimal("0.1"))
            penalty += weight * Decimal(str(count))

        # Score decreases with penalty
        score = max(Decimal("0"), Decimal("100") - (penalty * Decimal("5")))

        return score

    def _calculate_anomaly_score(self, anomalies: list[Any]) -> Decimal:
        """Calculate score based on open anomalies (higher = better)."""
        if not anomalies:
            return Decimal("100")

        # Each anomaly reduces score
        score = Decimal("100") - (Decimal(str(len(anomalies))) * Decimal("10"))

        return max(Decimal("0"), score)

    def _determine_risk_level(self, score: Decimal) -> str:
        """Determine risk level from score."""
        if score >= 80:
            return "LOW"
        elif score >= 60:
            return "MEDIUM"
        elif score >= 40:
            return "HIGH"
        else:
            return "CRITICAL"

    def _generate_recommendations(
            self,
            score: Decimal,
            events: list[Any],
            anomalies: list[Any],
    ) -> list[str]:
        """Generate actionable recommendations."""
        recommendations = []

        if score < 50:
            recommendations.append(
                "Immediate attention required - service health is degraded"
            )

        # Check for critical events
        critical_events = [e for e in events if e.severity == "CRITICAL"]
        if critical_events:
            recommendations.append(
                f"Review {len(critical_events)} critical event(s) immediately"
            )

        # Check for open anomalies
        if anomalies:
            recommendations.append(
                f"Investigate and resolve {len(anomalies)} open anomaly/anomalies"
            )

        if not recommendations:
            recommendations.append("Service is operating normally")

        return recommendations

    async def get_service_comparison(
            self,
            services: list[str],
            time_window_minutes: int = 60,
    ) -> dict[str, Any]:
        """
        Compare scores across multiple services.

        Args:
            services: List of service names
            time_window_minutes: Time window

        Returns:
            Comparison results
        """
        results = []

        for service in services:
            score_data = await self.calculate_score(service, time_window_minutes)
            results.append({
                "service": service,
                "score": score_data["overall_score"],
                "risk_level": score_data["risk_level"],
            })

        # Sort by score (ascending - lowest first)
        results.sort(key=lambda x: x["score"])

        return {
            "comparison": results,
            "best_performer": results[-1]["service"] if results else None,
            "needs_attention": results[0]["service"] if results else None,
        }
"""
AI Engine - Core AI service for contextual analysis.
Integrates with Groq and OpenAI for insights generation.
"""

from decimal import Decimal
from typing import Any

from app.config import settings
from app.core.logging import get_logger
from app.core.exceptions import AIServiceException

logger = get_logger(__name__)


class AIEngine:
    """
    AI Engine for generating contextual insights.

    Supports:
    - Groq (LLaMA 3.1)
    - OpenAI (GPT-4, GPT-3.5)
    """

    def __init__(self) -> None:
        self.groq_client = None
        self.openai_client = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize AI clients."""
        try:
            if settings.groq_api_key:
                from groq import Groq
                self.groq_client = Groq(api_key=settings.groq_api_key)
                logger.info("Groq client initialized")

            if settings.openai_api_key:
                import openai
                self.openai_client = openai.AsyncOpenAI(
                    api_key=settings.openai_api_key
                )
                logger.info("OpenAI client initialized")

            self._initialized = True

        except Exception as e:
            logger.error("Failed to initialize AI clients", error=str(e))
            raise AIServiceException("AIEngine", f"Initialization failed: {e}")

    async def generate_insight(
            self,
            context: dict[str, Any],
            insight_type: str = "ANOMALY_DETECTION",
    ) -> dict[str, Any]:
        """
        Generate an AI-powered insight.

        Args:
            context: Context data for analysis
            insight_type: Type of insight to generate

        Returns:
            Generated insight with confidence score
        """
        if not self._initialized:
            await self.initialize()

        prompt = self._build_prompt(context, insight_type)

        try:
            # Try Groq first (faster, cheaper)
            if self.groq_client:
                return await self._generate_with_groq(prompt, insight_type)

            # Fallback to OpenAI
            if self.openai_client:
                return await self._generate_with_openai(prompt, insight_type)

            raise AIServiceException("AIEngine", "No AI provider configured")

        except Exception as e:
            logger.error("Failed to generate insight", error=str(e))
            raise AIServiceException("AIEngine", str(e))

    async def _generate_with_groq(
            self,
            prompt: str,
            insight_type: str,
    ) -> dict[str, Any]:
        """Generate insight using Groq (LLaMA)."""
        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(insight_type),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=1000,
            )

            content = response.choices[0].message.content

            return self._parse_response(content, "groq", "llama-3.1-70b")

        except Exception as e:
            logger.warning("Groq generation failed, trying fallback", error=str(e))
            if self.openai_client:
                return await self._generate_with_openai(prompt, insight_type)
            raise

    async def _generate_with_openai(
            self,
            prompt: str,
            insight_type: str,
    ) -> dict[str, Any]:
        """Generate insight using OpenAI."""
        response = await self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": self._get_system_prompt(insight_type),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1000,
        )

        content = response.choices[0].message.content

        return self._parse_response(content, "openai", "gpt-4-turbo")

    def _build_prompt(
            self,
            context: dict[str, Any],
            insight_type: str,
    ) -> str:
        """Build prompt from context."""
        import json

        context_str = json.dumps(context, indent=2, default=str)

        return f"""
Analyze the following operational data and generate an insight.

Context Data:
{context_str}

Insight Type: {insight_type}

Provide your analysis in this JSON format:
{{
    "title": "Brief title of the insight",
    "summary": "One sentence summary",
    "description": "Detailed explanation",
    "confidence_score": 0.85,
    "recommendation_level": "INFO|WARNING|ACTION_REQUIRED|CRITICAL",
    "recommendation": "What should be done",
    "action_items": ["action 1", "action 2"],
    "anomaly_type": "Type of anomaly if detected"
}}
"""

    def _get_system_prompt(self, insight_type: str) -> str:
        """Get system prompt based on insight type."""
        prompts = {
            "ANOMALY_DETECTION": (
                "You are an expert in detecting operational anomalies. "
                "Analyze data patterns and identify unusual behavior. "
                "Be precise and actionable in your recommendations."
            ),
            "TREND_ANALYSIS": (
                "You are an expert in trend analysis. "
                "Identify patterns and predict future behavior. "
                "Provide clear, data-driven insights."
            ),
            "PREDICTION": (
                "You are an expert in predictive analytics. "
                "Analyze historical data to forecast future outcomes. "
                "Include confidence intervals when possible."
            ),
            "CORRELATION": (
                "You are an expert in event correlation. "
                "Find relationships between seemingly unrelated events. "
                "Explain causal chains and dependencies."
            ),
            "RISK_ASSESSMENT": (
                "You are an expert in risk assessment. "
                "Evaluate operational risks and their potential impact. "
                "Prioritize recommendations by urgency."
            ),
        }

        return prompts.get(
            insight_type,
            "You are an expert operational intelligence analyst.",
        )

    def _parse_response(
            self,
            content: str,
            provider: str,
            model: str,
    ) -> dict[str, Any]:
        """Parse AI response into structured format."""
        import json
        import re

        # Try to extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', content)

        if json_match:
            try:
                parsed = json.loads(json_match.group())

                # Ensure required fields
                return {
                    "title": parsed.get("title", "AI Generated Insight"),
                    "summary": parsed.get("summary"),
                    "description": parsed.get("description", content),
                    "confidence_score": Decimal(str(parsed.get("confidence_score", 0.7))),
                    "recommendation_level": parsed.get("recommendation_level", "INFO"),
                    "recommendation": parsed.get("recommendation"),
                    "action_items": parsed.get("action_items", []),
                    "anomaly_type": parsed.get("anomaly_type"),
                    "model_provider": provider,
                    "model_name": model,
                }
            except json.JSONDecodeError:
                pass

        # Fallback: use content as description
        return {
            "title": "AI Generated Insight",
            "description": content,
            "confidence_score": Decimal("0.5"),
            "recommendation_level": "INFO",
            "model_provider": provider,
            "model_name": model,
        }


# Singleton instance
_ai_engine: AIEngine | None = None


async def get_ai_engine() -> AIEngine:
    """Get or create AI engine instance."""
    global _ai_engine

    if _ai_engine is None:
        _ai_engine = AIEngine()
        await _ai_engine.initialize()

    return _ai_engine
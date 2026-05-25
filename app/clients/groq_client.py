"""
Groq API client for fast LLM inference.
Uses LLaMA 3.1 for AI operations.
"""

from typing import Any

from app.config import settings
from app.core.logging import get_logger
from app.core.exceptions import AIServiceException

logger = get_logger(__name__)


class GroqClient:
    """
    Client for Groq API.

    Provides fast inference with LLaMA models.
    """

    def __init__(self) -> None:
        self.client = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize Groq client."""
        if not settings.groq_api_key:
            logger.warning("Groq API key not configured")
            return

        try:
            from groq import Groq
            self.client = Groq(api_key=settings.groq_api_key)
            self._initialized = True
            logger.info("Groq client initialized")
        except Exception as e:
            logger.error("Failed to initialize Groq client", error=str(e))

    async def generate(
            self,
            prompt: str,
            system_prompt: str | None = None,
            model: str = "llama-3.1-70b-versatile",
            temperature: float = 0.3,
            max_tokens: int = 1000,
    ) -> dict[str, Any]:
        """
        Generate completion with Groq.

        Args:
            prompt: User prompt
            system_prompt: System instructions
            model: Model to use
            temperature: Sampling temperature
            max_tokens: Max tokens to generate

        Returns:
            Response with generated text
        """
        if not self._initialized:
            await self.initialize()

        if not self.client:
            raise AIServiceException("Groq", "Client not initialized")

        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            content = response.choices[0].message.content

            return {
                "content": content,
                "model": model,
                "provider": "groq",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            }

        except Exception as e:
            logger.error("Groq generation failed", error=str(e))
            raise AIServiceException("Groq", str(e))

    async def analyze(
            self,
            data: dict[str, Any],
            analysis_type: str = "general",
    ) -> dict[str, Any]:
        """
        Analyze data with Groq.

        Args:
            data: Data to analyze
            analysis_type: Type of analysis

        Returns:
            Analysis results
        """
        import json

        prompt = f"""
Analyze the following data and provide insights.

Data:
{json.dumps(data, indent=2, default=str)}

Analysis Type: {analysis_type}

Provide your analysis in JSON format.
"""

        system_prompt = (
            "You are an expert operational intelligence analyst. "
            "Provide structured, actionable insights."
        )

        result = await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
        )

        return result

    async def health_check(self) -> bool:
        """Check if Groq API is accessible."""
        if not self._initialized:
            await self.initialize()

        return self.client is not None


# Singleton
_groq_client: GroqClient | None = None


async def get_groq_client() -> GroqClient:
    """Get or create Groq client."""
    global _groq_client

    if _groq_client is None:
        _groq_client = GroqClient()
        await _groq_client.initialize()

    return _groq_client
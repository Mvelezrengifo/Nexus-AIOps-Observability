"""
OpenAI API client as fallback AI provider.
"""

from typing import Any

from app.config import settings
from app.core.logging import get_logger
from app.core.exceptions import AIServiceException

logger = get_logger(__name__)


class OpenAIClient:
    """
    Client for OpenAI API.

    Provides GPT-4 and GPT-3.5 inference as fallback.
    """

    def __init__(self) -> None:
        self.client = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize OpenAI client."""
        if not settings.openai_api_key:
            logger.warning("OpenAI API key not configured")
            return

        try:
            import openai
            self.client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
            self._initialized = True
            logger.info("OpenAI client initialized")
        except Exception as e:
            logger.error("Failed to initialize OpenAI client", error=str(e))

    async def generate(
            self,
            prompt: str,
            system_prompt: str | None = None,
            model: str = "gpt-4-turbo-preview",
            temperature: float = 0.3,
            max_tokens: int = 1000,
    ) -> dict[str, Any]:
        """
        Generate completion with OpenAI.

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
            raise AIServiceException("OpenAI", "Client not initialized")

        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            content = response.choices[0].message.content

            return {
                "content": content,
                "model": model,
                "provider": "openai",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            }

        except Exception as e:
            logger.error("OpenAI generation failed", error=str(e))
            raise AIServiceException("OpenAI", str(e))

    async def generate_with_vision(
            self,
            prompt: str,
            image_url: str,
            model: str = "gpt-4-vision-preview",
    ) -> dict[str, Any]:
        """
        Generate completion with vision support.

        Args:
            prompt: User prompt
            image_url: URL of image to analyze
            model: Vision model

        Returns:
            Response with analysis
        """
        if not self._initialized:
            await self.initialize()

        if not self.client:
            raise AIServiceException("OpenAI", "Client not initialized")

        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": image_url}},
                        ],
                    }
                ],
                max_tokens=1000,
            )

            return {
                "content": response.choices[0].message.content,
                "model": model,
                "provider": "openai",
            }

        except Exception as e:
            logger.error("OpenAI vision generation failed", error=str(e))
            raise AIServiceException("OpenAI", str(e))

    async def health_check(self) -> bool:
        """Check if OpenAI API is accessible."""
        if not self._initialized:
            await self.initialize()

        return self.client is not None


# Singleton
_openai_client: OpenAIClient | None = None


async def get_openai_client() -> OpenAIClient:
    """Get or create OpenAI client."""
    global _openai_client

    if _openai_client is None:
        _openai_client = OpenAIClient()
        await _openai_client.initialize()

    return _openai_client
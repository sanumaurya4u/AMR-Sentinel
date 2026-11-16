"""OpenRouter API client for resilient multi-provider LLM fallback."""
from typing import Any

import httpx
from app.config import get_settings


class OpenRouterClient:
    """Async client for OpenRouter inference endpoint."""

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self):
        self.settings = get_settings()

    @property
    def is_configured(self) -> bool:
        """Check if OpenRouter API key is configured."""
        return bool(self.settings.OPENROUTER_API_KEY and len(self.settings.OPENROUTER_API_KEY) > 10)

    async def generate_completion(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float = 0.0,
        response_format: dict[str, str] | None = None,
    ) -> str:
        """Call OpenRouter completions endpoint with automatic timeout handling."""
        if not self.is_configured:
            raise RuntimeError("OPENROUTER_API_KEY is not configured in settings.")

        target_model = model or self.settings.OPENROUTER_MODEL
        headers = {
            "Authorization": f"Bearer {self.settings.OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://amr-sentinel.vercel.app",
            "X-Title": "AMR Sentinel AI",
            "Content-Type": "application/json",
        }

        payload: dict[str, Any] = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
        }
        if response_format:
            payload["response_format"] = response_format

        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(self.BASE_URL, json=payload, headers=headers)
            if resp.status_code != 200:
                raise RuntimeError(f"OpenRouter returned status {resp.status_code}: {resp.text}")

            data = resp.json()
            return data["choices"][0]["message"]["content"]


_openrouter_instance: OpenRouterClient | None = None


def get_openrouter_client() -> OpenRouterClient:
    """Singleton getter for OpenRouterClient."""
    global _openrouter_instance
    if _openrouter_instance is None:
        _openrouter_instance = OpenRouterClient()
    return _openrouter_instance

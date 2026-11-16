"""LLM provider routing package supporting Gemini and OpenRouter fallback."""
from app.llm.openrouter import OpenRouterClient, get_openrouter_client

__all__ = ["OpenRouterClient", "get_openrouter_client"]

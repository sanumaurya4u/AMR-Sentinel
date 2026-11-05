"""Application configuration settings for AMR Sentinel API."""
import json
from functools import lru_cache
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    PROJECT_NAME: str = "AMR Sentinel AI"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # CORS origins
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://amr-sentinel.vercel.app",
    ]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> list[str]:
        """Support both JSON list format and comma-separated string format in env files."""
        if isinstance(v, str):
            v_stripped = v.strip()
            if v_stripped.startswith("[") and v_stripped.endswith("]"):
                try:
                    return json.loads(v_stripped)
                except (json.JSONDecodeError, TypeError):
                    return [i.strip() for i in v_stripped.strip("[]").split(",") if i.strip()]
            return [i.strip() for i in v_stripped.split(",") if i.strip()]
        if isinstance(v, list):
            return v
        return []

    # Supabase credentials (optional for pure offline fallback)
    SUPABASE_URL: str = "https://oqtgkptpmxldkxwybtls.supabase.co"
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    SUPABASE_JWT_SECRET: str = ""

    # Assistive AI (Optional Gemini API key for OCR/intake)
    GEMINI_API_KEY: str = ""

    # Active clinical rule set version
    ACTIVE_RULE_SET_VERSION: str = "1.0.0"
    DEMO_MODE: bool = True


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()

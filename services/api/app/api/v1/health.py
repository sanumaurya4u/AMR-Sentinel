"""Health and liveness endpoint."""
from app.config import get_settings
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Health and liveness endpoint returning service metadata with zero PHI."""
    settings = get_settings()
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "active_rule_set_version": settings.ACTIVE_RULE_SET_VERSION,
        "demo_mode": settings.DEMO_MODE,
        "engine_mode": "deterministic_isolated",
    }

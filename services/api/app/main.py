"""Main FastAPI application entrypoint for AMR Sentinel AI."""
import time
import uuid

from app.api.v1.agent import router as agent_router
from app.api.v1.audits import router as audits_router
from app.api.v1.extractions import router as extractions_router
from app.api.v1.health import router as health_router
from app.api.v1.metrics import router as metrics_router
from app.api.v1.rag import router as rag_router
from app.config import get_settings
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Clinician-assistive antimicrobial prescription auditing platform. "
        "Deterministic clinical evaluation core strictly separated from stochastic AI intake. "
        "This platform is assistive decision support; it does not diagnose or prescribe."
    ),
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url=None,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_and_trace_headers(request: Request, call_next):
    """Add trace ID, timing, and security headers while preventing PHI leakage in logs."""
    trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
    start_time = time.perf_counter()

    try:
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Trace-ID"] = trace_id
        response.headers["X-Response-Time-Sec"] = f"{process_time:.4f}"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response
    except Exception:  # noqa: BLE001
        # Never leak exception tracebacks to client in clinical API
        return JSONResponse(
            status_code=500,
            content={
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred during processing. Please verify inputs.",
                "trace_id": trace_id,
            },
            headers={"X-Trace-ID": trace_id},
        )


# Include routes
app.include_router(health_router)
app.include_router(health_router, prefix="/api/v1")
app.include_router(audits_router, prefix="/v1")
app.include_router(audits_router, prefix="/api/v1")
app.include_router(extractions_router, prefix="/v1")
app.include_router(extractions_router, prefix="/api/v1")
app.include_router(metrics_router, prefix="/v1")
app.include_router(metrics_router, prefix="/api/v1")
app.include_router(agent_router, prefix="/v1")
app.include_router(agent_router, prefix="/api/v1")
app.include_router(rag_router, prefix="/v1")
app.include_router(rag_router, prefix="/api/v1")

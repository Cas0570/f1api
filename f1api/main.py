from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from f1api.api.router import api_router
from f1api.core.config import settings
from f1api.core.errors import init_exception_handlers

app = FastAPI(
    title="F1 API",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# install global error handlers
init_exception_handlers(app)


# healthz (keep as-is)
@app.get("/healthz", tags=["meta"])
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics", tags=["meta"], response_class=PlainTextResponse)
def metrics() -> str:
    """Prometheus-friendly metrics stub."""

    return "# Metrics not implemented yet\n"


# main API
app.include_router(api_router)

# --- Dev-only debug endpoint to simulate a 500 for tests ---
if settings.app_env != "production":

    @app.get("/api/v1/_debug/boom")  # pragma: no cover (covered via tests explicitly)
    def boom() -> None:
        # intentionally raise an unhandled error
        raise RuntimeError("Kaboom")

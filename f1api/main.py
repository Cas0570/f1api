from fastapi import FastAPI
from f1api.api.router import api_router

app = FastAPI(
    title="F1 API",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",  # reserve /api/v1 base for routes later
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(api_router)


@app.get("/healthz", tags=["meta"])
def healthz() -> dict[str, str]:
    """
    Liveness probe. Returns {"status": "ok"} if the app is running.
    """
    return {"status": "ok"}

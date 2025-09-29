from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def _payload(
    request: Request,
    status: int,
    error: str,
    detail: Any,
) -> dict[str, Any]:
    return {
        "status": status,
        "error": error,
        "detail": detail,
        "path": request.url.path,
        "timestamp": datetime.now(UTC).isoformat(),
    }


def init_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def _(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_payload(
                request=request,
                status=exc.status_code,
                error="HTTPException",
                detail=exc.detail,
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def _(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=_payload(
                request=request,
                status=422,
                error="ValidationError",
                detail=exc.errors(),
            ),
        )

    @app.exception_handler(Exception)
    async def _(request: Request, _: Exception) -> JSONResponse:
        # We’ll wire structured logging in a later step
        return JSONResponse(
            status_code=500,
            content=_payload(
                request=request,
                status=500,
                error="InternalServerError",
                detail="An unexpected error occurred.",
            ),
        )

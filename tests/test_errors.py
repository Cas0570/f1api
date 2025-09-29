import pytest
from httpx import ASGITransport, AsyncClient

from f1api.main import app


@pytest.mark.asyncio
async def test_404_json_shape() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/does-not-exist")
    assert resp.status_code == 404
    body = resp.json()
    # expected shape
    for key in ("status", "error", "detail", "path", "timestamp"):
        assert key in body
    assert body["status"] == 404
    assert body["error"] == "HTTPException"
    assert body["path"] == "/api/v1/does-not-exist"


@pytest.mark.asyncio
async def test_unhandled_exception_returns_500() -> None:
    # dev-only route is available because default APP_ENV=development
    # Important: prevent httpx from re-raising app exceptions so we get a 500 response
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/_debug/boom")
    assert resp.status_code == 500
    body = resp.json()
    assert body["status"] == 500
    assert body["error"] == "InternalServerError"
    assert body["path"] == "/api/v1/_debug/boom"

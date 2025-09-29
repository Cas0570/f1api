import pytest
import httpx
from httpx import ASGITransport

from f1api.main import app


@pytest.mark.asyncio
async def test_healthz_ok():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

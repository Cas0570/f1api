import pytest
import httpx
from httpx import ASGITransport
from f1api.main import app


@pytest.mark.asyncio
async def test_list_seasons_seeded():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/seasons")
    assert resp.status_code == 200
    data = resp.json()
    assert any(s["year"] == 2024 for s in data)

import pytest
import httpx
from httpx import ASGITransport
from f1api.main import app


@pytest.mark.asyncio
async def test_list_drivers_seeded():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/drivers")
    assert resp.status_code == 200
    data = resp.json()
    assert any(d["ref"] == "max_verstappen" for d in data)

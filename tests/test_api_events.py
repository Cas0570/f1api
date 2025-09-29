import pytest
import httpx
from httpx import ASGITransport
from f1api.main import app


@pytest.mark.asyncio
async def test_list_events_filter_by_year():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/events?season_year=2024")
    assert resp.status_code == 200
    data = resp.json()
    assert any(e["name"] == "Bahrain Grand Prix" for e in data)

import httpx
import pytest
from httpx import ASGITransport

from f1api.main import app


@pytest.mark.asyncio
async def test_list_events_filter_by_year() -> None:
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/events?season_year=2024")
    assert resp.status_code == 200
    data = resp.json()
    assert any(e["name"] == "Bahrain Grand Prix" for e in data)


@pytest.mark.asyncio
async def test_get_event_by_id() -> None:
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        list_resp = await client.get("/api/v1/events?season_year=2024")
        eid = list_resp.json()[0]["id"]

        resp = await client.get(f"/api/v1/events/{eid}")
    assert resp.status_code == 200
    assert "name" in resp.json()


@pytest.mark.asyncio
async def test_get_event_not_found() -> None:
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/events/99999")
    assert resp.status_code == 404

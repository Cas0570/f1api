import httpx
import pytest
from httpx import ASGITransport

from f1api.main import app


@pytest.mark.asyncio
async def test_list_seasons_seeded() -> None:
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/seasons")
    assert resp.status_code == 200
    data = resp.json()
    assert any(s["year"] == 2024 for s in data)


@pytest.mark.asyncio
async def test_get_season_by_id() -> None:
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        list_resp = await client.get("/api/v1/seasons")
        sid = list_resp.json()[0]["id"]

        resp = await client.get(f"/api/v1/seasons/{sid}")
    assert resp.status_code == 200
    assert "year" in resp.json()


@pytest.mark.asyncio
async def test_get_season_not_found() -> None:
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/seasons/99999")
    assert resp.status_code == 404

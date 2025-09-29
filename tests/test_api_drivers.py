import httpx
import pytest
from httpx import ASGITransport

from f1api.main import app


@pytest.mark.asyncio
async def test_list_drivers_seeded() -> None:
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/drivers")
    assert resp.status_code == 200
    data = resp.json()
    assert any(d["ref"] == "max_verstappen" for d in data)


@pytest.mark.asyncio
async def test_filter_driver_by_code() -> None:
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/drivers?code=VER")
    assert resp.status_code == 200
    data = resp.json()
    assert any(d["code"] == "VER" for d in data)


@pytest.mark.asyncio
async def test_get_driver_not_found() -> None:
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/drivers/99999")
    assert resp.status_code == 404

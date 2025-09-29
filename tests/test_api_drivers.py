import pytest
from httpx import ASGITransport, AsyncClient

from f1api.main import app


@pytest.mark.asyncio
async def test_list_drivers_seeded() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/drivers")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert "page" in data
    assert "pages" in data
    assert any(d["ref"] == "max_verstappen" for d in data["items"])


@pytest.mark.asyncio
async def test_filter_driver_by_code() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/drivers?code=VER")
    assert resp.status_code == 200
    data = resp.json()
    assert any(d["code"] == "VER" for d in data["items"])


@pytest.mark.asyncio
async def test_get_driver_not_found() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/drivers/99999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_drivers_pagination_metadata() -> None:
    """Test pagination metadata is correct."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/drivers?limit=1&offset=0")
    assert resp.status_code == 200
    data = resp.json()
    assert data["limit"] == 1
    assert data["offset"] == 0
    assert data["page"] == 1
    assert data["total"] >= 2  # At least VER and PER
    assert len(data["items"]) == 1

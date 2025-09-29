import pytest
from httpx import ASGITransport, AsyncClient

from f1api.main import app


@pytest.mark.asyncio
async def test_driver_standings_2024() -> None:
    """Test driver standings endpoint returns seeded 2024 data."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/standings/drivers?season_year=2024")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert len(data["items"]) >= 2
    # Verify VER is P1 with 25 points
    ver_standing = next((s for s in data["items"] if s["driver_code"] == "VER"), None)
    assert ver_standing is not None
    assert ver_standing["position"] == 1
    assert ver_standing["points"] == 25.0
    assert ver_standing["wins"] == 1


@pytest.mark.asyncio
async def test_constructor_standings_2024() -> None:
    """Test constructor standings endpoint returns seeded 2024 data."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/standings/constructors?season_year=2024")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert len(data["items"]) >= 1
    # Verify RBR is P1 with combined points (25 + 18 = 43)
    rbr_standing = next((s for s in data["items"] if s["team_ref"] == "red_bull_racing"), None)
    assert rbr_standing is not None
    assert rbr_standing["position"] == 1
    assert rbr_standing["points"] == 43.0
    assert rbr_standing["wins"] == 1


@pytest.mark.asyncio
async def test_standings_invalid_season() -> None:
    """Test standings returns 404 for non-existent season."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/standings/drivers?season_year=1999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_standings_requires_season_year() -> None:
    """Test standings endpoint requires season_year parameter."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/standings/drivers")
    assert resp.status_code == 422

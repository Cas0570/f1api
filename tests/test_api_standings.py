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
    ver_standing = next((s for s in data["items"] if s["driver_code"] == "VER"), None)
    assert ver_standing is not None
    assert ver_standing["position"] == 1
    assert ver_standing["points"] == 118.0
    assert ver_standing["wins"] == 4


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
    rbr_standing = next((s for s in data["items"] if s["team_ref"] == "red_bull_racing"), None)
    assert rbr_standing is not None
    assert rbr_standing["position"] == 1
    assert rbr_standing["points"] == 209.0
    assert rbr_standing["wins"] == 4


@pytest.mark.asyncio
async def test_driver_standings_comprehensive() -> None:
    """Test comprehensive standings show realistic 2024 battle."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/standings/drivers?season_year=2024&limit=5")
    assert resp.status_code == 200
    data = resp.json()

    # Verify top 5 drivers after 6 races
    assert len(data["items"]) == 5

    # P1: Max Verstappen
    assert data["items"][0]["driver_code"] == "VER"
    assert data["items"][0]["points"] == 118.0
    assert data["items"][0]["wins"] == 4

    # P2: Sergio Pérez
    assert data["items"][1]["driver_code"] == "PER"
    assert data["items"][1]["points"] == 91.0

    # P3-P5: Should include LEC, NOR, SAI in some order
    top5_codes = {d["driver_code"] for d in data["items"][:5]}
    assert {"VER", "PER", "LEC", "NOR", "SAI"}.issubset(top5_codes)


@pytest.mark.asyncio
async def test_constructor_standings_comprehensive() -> None:
    """Test constructor standings show realistic team battle."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/standings/constructors?season_year=2024&limit=3")
    assert resp.status_code == 200
    data = resp.json()

    # Verify top 3 teams after 6 races
    assert len(data["items"]) == 3

    # P1: Red Bull Racing (dominant)
    assert data["items"][0]["team_ref"] == "red_bull_racing"
    assert data["items"][0]["points"] == 209.0
    assert data["items"][0]["wins"] == 4

    # P2-P3: Ferrari and McLaren battle
    top3_teams = {t["team_ref"] for t in data["items"][:3]}
    assert {"red_bull_racing", "ferrari", "mclaren"}.issubset(top3_teams)


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
    assert resp.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_standings_pagination() -> None:
    """Test standings pagination works correctly."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Get first page
        resp1 = await client.get("/api/v1/standings/drivers?season_year=2024&limit=5&offset=0")
        assert resp1.status_code == 200
        data1 = resp1.json()
        assert len(data1["items"]) == 5
        assert data1["page"] == 1

        # Get second page
        resp2 = await client.get("/api/v1/standings/drivers?season_year=2024&limit=5&offset=5")
        assert resp2.status_code == 200
        data2 = resp2.json()
        assert data2["page"] == 2

        # Verify no overlap
        page1_drivers = {d["driver_id"] for d in data1["items"]}
        page2_drivers = {d["driver_id"] for d in data2["items"]}
        assert len(page1_drivers & page2_drivers) == 0  # No overlap

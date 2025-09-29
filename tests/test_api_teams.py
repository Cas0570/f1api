import pytest
from httpx import ASGITransport, AsyncClient

from f1api.main import app


@pytest.mark.asyncio
async def test_list_teams_seeded() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/teams")
    assert resp.status_code == 200
    data = resp.json()
    assert any(t["ref"] == "red_bull_racing" for t in data)


@pytest.mark.asyncio
async def test_get_team_by_id() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        list_resp = await client.get("/api/v1/teams")
        tid = list_resp.json()[0]["id"]

        resp = await client.get(f"/api/v1/teams/{tid}")
    assert resp.status_code == 200
    assert "ref" in resp.json()


@pytest.mark.asyncio
async def test_get_team_not_found() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/teams/99999")
    assert resp.status_code == 404

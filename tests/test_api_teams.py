import pytest
import httpx
from httpx import ASGITransport
from f1api.main import app


@pytest.mark.asyncio
async def test_list_teams_seeded():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/teams")
    assert resp.status_code == 200
    data = resp.json()
    assert any(t["ref"] == "red_bull_racing" for t in data)

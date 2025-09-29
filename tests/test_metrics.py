import pytest
from httpx import ASGITransport, AsyncClient

from f1api.main import app


@pytest.mark.asyncio
async def test_metrics_stub_returns_placeholder() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/metrics")

    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/plain")
    assert resp.text == "# Metrics not implemented yet\n"

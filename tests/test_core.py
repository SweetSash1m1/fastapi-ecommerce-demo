import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_healthcheck(ac: AsyncClient) -> None:
    response = await ac.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "service is running"}

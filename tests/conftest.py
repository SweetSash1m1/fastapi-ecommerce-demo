from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from src.core.bootstrap import create_app


@pytest.fixture
async def ac() -> AsyncGenerator[AsyncClient, None]:
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

from httpx import AsyncClient, ASGITransport
import pytest_asyncio

from app.main import app


@pytest_asyncio.fixture
async def anonymous_client():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://localhost/"
    ) as ac:
        yield ac

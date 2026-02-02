import pytest
from typing import AsyncGenerator
from infra.clients.common import AsyncHTTPSession


@pytest.fixture
async def async_http_session() -> AsyncGenerator[AsyncHTTPSession, None]:
    async with AsyncHTTPSession() as session:
        yield session

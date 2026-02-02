import pytest
from unittest.mock import AsyncMock
from infra.clients.dota_market.gateway import (
    DotaMarketGateway,
    IDotaMarketClient,
    IRateLimiter,
)


@pytest.fixture
def dota_market_client() -> IDotaMarketClient:
    return AsyncMock()


@pytest.fixture
def rate_limiter() -> IRateLimiter:
    limiter = AsyncMock()
    limiter.wait = AsyncMock()
    return limiter


@pytest.mark.asyncio
async def test_get_item_history(dota_market_client, rate_limiter):
    fake_result = "parsed"
    dota_market_client.get_item_history.return_value = fake_result

    gateway = DotaMarketGateway(client=dota_market_client, rate_limiter=rate_limiter)
    
    result = await gateway.get_item_history(1, 2)

    rate_limiter.wait.assert_awaited_once()
    dota_market_client.get_item_history.assert_awaited_once_with(1, 2)
    assert result == fake_result


@pytest.mark.asyncio
async def test_get_sell_offers(dota_market_client, rate_limiter):
    fake_result = "parsed"
    dota_market_client.get_sell_offers.return_value = fake_result

    gateway = DotaMarketGateway(client=dota_market_client, rate_limiter=rate_limiter)

    result = await gateway.get_sell_offers(1, 2)

    rate_limiter.wait.assert_awaited_once()
    dota_market_client.get_sell_offers.assert_awaited_once_with(1, 2)
    assert result == fake_result


@pytest.mark.asyncio
async def test_get_buy_offers(dota_market_client, rate_limiter):
    fake_result = "parsed"
    dota_market_client.get_buy_offers.return_value = fake_result

    gateway = DotaMarketGateway(client=dota_market_client, rate_limiter=rate_limiter)

    result = await gateway.get_buy_offers(1, 2)

    rate_limiter.wait.assert_awaited_once()
    dota_market_client.get_buy_offers.assert_awaited_once_with(1, 2)
    assert result == fake_result

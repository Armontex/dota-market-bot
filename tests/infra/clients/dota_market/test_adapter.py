import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from infra.clients.dota_market.adapter import DotaMarketClient
from infra.clients.common import RequestMethod
from infra.clients.dota_market.schemas import (
    ItemHistorySchema,
    SellOffersSchema,
    BuyOffersSchema,
)


@pytest.mark.asyncio
async def test_request_calls_session_correctly():
    session = AsyncMock()
    session.request.return_value.json.return_value = {"data": 123}

    client = DotaMarketClient("api-key", "https://api.test/", session)

    # Вызываем _request
    resp = await client._request(RequestMethod.GET, "endpoint/")

    session.request.assert_awaited_once_with(
        RequestMethod.GET,
        "https://api.test/endpoint/",
        headers={"X-API-KEY": "api-key"},
    )
    assert resp == session.request.return_value


@pytest.mark.asyncio
async def test_get_item_history():
    fake_json = {"field": "value"}

    response = MagicMock()
    response.json.return_value = fake_json

    session = AsyncMock()
    session.request.return_value = response

    client = DotaMarketClient("api-key", "https://api.test/", session)

    model_validate = MagicMock()
    model_validate.return_value = "parsed"
    with patch.object(ItemHistorySchema, "model_validate", new=model_validate):
        result = await client.get_item_history(1, 2)

        session.request.assert_awaited_once()
        args, _ = session.request.call_args
        assert "ItemHistory/1_2/" in args[1]
        
        model_validate.assert_called_once_with(fake_json)
        assert result == "parsed"


@pytest.mark.asyncio
async def test_get_sell_offers():
    fake_json = {"field": "value"}

    response = MagicMock()
    response.json.return_value = fake_json

    session = AsyncMock()
    session.request.return_value = response

    client = DotaMarketClient("api-key", "https://api.test/", session)

    model_validate = MagicMock()
    model_validate.return_value = "parsed"
    with patch.object(SellOffersSchema, "model_validate", new=model_validate):
        result = await client.get_sell_offers(1, 2)

        session.request.assert_awaited_once()
        args, _ = session.request.call_args
        assert "SellOffers/1_2/" in args[1]

        model_validate.assert_called_once_with(fake_json)
        assert result == "parsed"


@pytest.mark.asyncio
async def test_get_buy_offers():
    fake_json = {"field": "value"}

    response = MagicMock()
    response.json.return_value = fake_json

    session = AsyncMock()
    session.request.return_value = response

    client = DotaMarketClient("api-key", "https://api.test/", session)

    model_validate = MagicMock()
    model_validate.return_value = "parsed"
    with patch.object(BuyOffersSchema, "model_validate", new=model_validate):
        result = await client.get_buy_offers(1, 2)

        session.request.assert_awaited_once()
        args, _ = session.request.call_args
        assert "BuyOffers/1_2/" in args[1]

        model_validate.assert_called_once_with(fake_json)
        assert result == "parsed"


async def test_request_preserves_custom_headers():
    session = AsyncMock()
    session.request.return_value.json.return_value = {}

    client = DotaMarketClient("api-key", "https://api.test/", session)

    await client._request(
        RequestMethod.GET,
        "endpoint/",
        headers={"Custom": "1"},
    )

    session.request.assert_awaited_once_with(
        RequestMethod.GET,
        "https://api.test/endpoint/",
        headers={"Custom": "1"},
    )

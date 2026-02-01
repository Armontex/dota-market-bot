from urllib.parse import urljoin
from infra.clients.common import RequestMethod
from infra.clients.common.decorators import handle_api_errors
from .schemas import ItemHistorySchema, SellOffersSchema, BuyOffersSchema
from .protocols import IAsyncHTTPSession


class DotaMarketClient:

    BASE_URL = "https://market.dota2.net/api/"

    def __init__(self, api_key: str, session: IAsyncHTTPSession) -> None:
        self._session = session
        self._headers = {"X-API-KEY": api_key}

    @handle_api_errors
    async def _request(self, method: RequestMethod, endpoint: str, **kwargs):
        url = urljoin(self.BASE_URL, endpoint)
        kwargs.setdefault("headers", self._headers)
        return await self._session.request(method, url, **kwargs)

    async def get_item_history(
        self, class_id: int, instance_id: int
    ) -> ItemHistorySchema:
        endpoint = f"/ItemHistory/{class_id}_{instance_id}/"
        resp = await self._request(RequestMethod.GET, endpoint)
        return ItemHistorySchema.model_validate(resp.json())

    async def get_sell_offers(
        self, class_id: int, instance_id: int
    ) -> SellOffersSchema:
        endpoint = f"/SellOffers/{class_id}_{instance_id}/"
        resp = await self._request(RequestMethod.GET, endpoint)
        return SellOffersSchema.model_validate(resp.json())

    async def get_buy_offers(self, class_id: int, instance_id: int) -> BuyOffersSchema:
        endpoint = f"/BuyOffers/{class_id}_{instance_id}/"
        resp = await self._request(RequestMethod.GET, endpoint)
        return BuyOffersSchema.model_validate(resp.json())



from urllib.parse import urljoin
from common.decorators import handle_api_errors
from .schemas import ItemHistorySchema, SellOffersSchema, BuyOffersSchema
from .protocols import IAsyncHTTPSession, HTTPRequest


class DotaMarketClient:

    def __init__(
        self,
        api_key: str,
        base_url: str,
        session: IAsyncHTTPSession,
    ) -> None:
        '''Этот метод инициализирует объект с заданными значениями ключа API, базового URL и сеанса HTTP.
        
        Parameters
        ----------
        api_key : str
            api_key: ключ API, необходимый для аутентификации запросов к API.
        base_url : str
            base_url: URL-адрес базового ресурса, к которому будет осуществляться доступ через API.
        session : IAsyncHTTPSession
            session - это объект сеанса для выполнения асинхронных HTTP-запросов.
        '''
        self._session = session
        self._base_url = base_url
        self._headers = {"X-API-KEY": api_key}

    @handle_api_errors
    async def _request(self, method: HTTPRequest, endpoint: str, **kwargs):
        url = urljoin(self._base_url, endpoint)
        kwargs.setdefault("headers", self._headers)
        return await self._session.request(method, url, **kwargs)

    async def get_item_history(
        self, class_id: int, instance_id: int
    ) -> ItemHistorySchema:
        endpoint = f"ItemHistory/{class_id}_{instance_id}/"
        resp = await self._request("GET", endpoint)
        return ItemHistorySchema.model_validate(resp.json())

    async def get_sell_offers(

        self, class_id: int, instance_id: int
    ) -> SellOffersSchema:
        endpoint = f"SellOffers/{class_id}_{instance_id}/"
        resp = await self._request("GET", endpoint)
        return SellOffersSchema.model_validate(resp.json())

    async def get_buy_offers(self, class_id: int, instance_id: int) -> BuyOffersSchema:
        endpoint = f"BuyOffers/{class_id}_{instance_id}/"
        resp = await self._request("GET", endpoint)
        return BuyOffersSchema.model_validate(resp.json())

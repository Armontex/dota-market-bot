from typing import Protocol, Any
from infra.clients.common import RequestMethod
from .schemas import ItemHistorySchema, SellOffersSchema, BuyOffersSchema


class IResponse(Protocol):

    def json(**kwargs) -> Any: ...


class IAsyncHTTPSession(Protocol):

    async def request(self, method: RequestMethod, url: str, **kwargs) -> IResponse: ...


class IRateLimiter(Protocol):

    async def wait(self) -> None: ...


class IDotaMarketClient(Protocol):

    async def get_item_history(
        self, class_id: int, instance_id: int
    ) -> ItemHistorySchema: ...

    async def get_sell_offers(
        self, class_id: int, instance_id: int
    ) -> SellOffersSchema: ...

    async def get_buy_offers(
        self, class_id: int, instance_id: int
    ) -> BuyOffersSchema: ...

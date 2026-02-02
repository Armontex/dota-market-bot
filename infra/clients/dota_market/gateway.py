from ..common.protocols import IRateLimiter
from ..common.decorators import limit_rate
from .protocols import IDotaMarketClient
from .schemas import ItemHistorySchema, SellOffersSchema, BuyOffersSchema


class DotaMarketGateway:

    def __init__(self, client: IDotaMarketClient, rate_limiter: IRateLimiter) -> None:
        self._client = client
        self._rate_limiter = rate_limiter

    @limit_rate()
    async def get_item_history(
        self, class_id: int, instance_id: int
    ) -> ItemHistorySchema:
        return await self._client.get_item_history(class_id, instance_id)

    @limit_rate()
    async def get_sell_offers(
        self, class_id: int, instance_id: int
    ) -> SellOffersSchema:
        return await self._client.get_sell_offers(class_id, instance_id)

    @limit_rate()
    async def get_buy_offers(self, class_id: int, instance_id: int) -> BuyOffersSchema:
        return await self._client.get_buy_offers(class_id, instance_id)

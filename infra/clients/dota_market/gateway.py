from infra.clients.common import RateLimiter
from .protocols import IDotaMarketClient
from .schemas import ItemHistorySchema, SellOffersSchema, BuyOffersSchema


class DotaMarketGateway:

    def __init__(self, client: IDotaMarketClient, rate_limiter: RateLimiter) -> None:
        self._client = client
        self._limiter = rate_limiter

    async def get_item_history(
        self, class_id: int, instance_id: int
    ) -> ItemHistorySchema:
        await self._limiter.wait()
        return await self._client.get_item_history(class_id, instance_id)

    async def get_sell_offers(
        self, class_id: int, instance_id: int
    ) -> SellOffersSchema:
        await self._limiter.wait()
        return await self._client.get_sell_offers(class_id, instance_id)

    async def get_buy_offers(self, class_id: int, instance_id: int) -> BuyOffersSchema:
        await self._limiter.wait()
        return await self._client.get_buy_offers(class_id, instance_id)



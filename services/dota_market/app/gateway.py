from ..infra.client import (
    DotaMarketClient,
    BuyOffersSchema,
    SellOffersSchema,
    ItemHistorySchema,
)
from ..infra.rate_limiter import RateLimiter
from common.decorators import limit_rate_method


class DotaMarketGateway:

    def __init__(self, client: DotaMarketClient, rate_limiter: RateLimiter) -> None:
        self._client = client
        self._rate_limiter = rate_limiter

    @limit_rate_method()
    async def get_item_history(
        self, class_id: int, instance_id: int
    ) -> ItemHistorySchema:
        return await self._client.get_item_history(class_id, instance_id)

    @limit_rate_method()
    async def get_sell_offers(
        self, class_id: int, instance_id: int
    ) -> SellOffersSchema:
        return await self._client.get_sell_offers(class_id, instance_id)

    @limit_rate_method()
    async def get_buy_offers(self, class_id: int, instance_id: int) -> BuyOffersSchema:
        return await self._client.get_buy_offers(class_id, instance_id)

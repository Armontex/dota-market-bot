from ..app.factory import DotaMarketFactory
from ..infra.client.protocols import IAsyncHTTPSession
from ..infra.client import (
    BuyOffersSchema,
    SellOffersSchema,
    ItemHistorySchema,
)


class DotaMarketService:

    def __init__(self, api_key: str, session: IAsyncHTTPSession) -> None:
        self._gateway = DotaMarketFactory.get(api_key, session)

    async def get_item_history(
        self, class_id: int, instance_id: int
    ) -> ItemHistorySchema:
        return await self._gateway.get_item_history(class_id, instance_id)

    async def get_sell_offers(
        self, class_id: int, instance_id: int
    ) -> SellOffersSchema:
        return await self._gateway.get_sell_offers(class_id, instance_id)

    async def get_buy_offers(self, class_id: int, instance_id: int) -> BuyOffersSchema:
        return await self._gateway.get_buy_offers(class_id, instance_id)

from infra.clients.common import AsyncHTTPClient, RateLimiter, RequestMethod
from infra.clients.common.decorators import handle_api_errors
from .schemas import ItemHistorySchema, SellOffersSchema, BuyOffersSchema


class DotaMarketClient:

    def __init__(
        self, api_key: str, session: AsyncHTTPClient, rate_limiter: RateLimiter
    ) -> None:
        self._session = session
        self._limiter = rate_limiter
        self._headers = {"X-API-KEY": api_key}

    @handle_api_errors
    async def _request(self, method: RequestMethod, endpoint: str, **kwargs):
        kwargs.setdefault("headers", self._headers)
        await self._limiter.wait()
        return await self._session.request(method, endpoint, **kwargs)

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
    
    async def get_buy_offers(
        self, class_id: int, instance_id: int
    ) -> BuyOffersSchema:
        endpoint = f"/BuyOffers/{class_id}_{instance_id}/"
        resp = await self._request(RequestMethod.GET, endpoint)
        return BuyOffersSchema.model_validate(resp.json())


class DotaMarketClientFactory:
    DEFAULT_RPS = 5
    BASE_URL = "https://market.dota2.net/api/"

    _session: AsyncHTTPClient | None = None
    _limiters: dict[str, RateLimiter] = {}

    @classmethod
    async def setup(cls) -> None:
        if not cls._session:
            cls._session = AsyncHTTPClient(base_url=cls.BASE_URL)
            await cls._session.__aenter__()

    @classmethod
    async def close(cls) -> None:
        if cls._session:
            await cls._session.__aexit__(None, None, None)
            cls._session = None

    @classmethod
    async def get(cls, api_key: str) -> DotaMarketClient:
        if not cls._session:
            raise RuntimeError(
                "DotaMarketClientFactory is not initialized."
                "Call `await DotaMarketClientFactory.setup()` when the application starts."
            )
        limiter = cls._get_limiter(api_key)
        return DotaMarketClient(
            api_key=api_key, session=cls._session, rate_limiter=limiter
        )

    @classmethod
    def _get_limiter(cls, api_key: str) -> RateLimiter:
        if api_key not in cls._limiters:
            cls._limiters[api_key] = RateLimiter(cls.DEFAULT_RPS)
        return cls._limiters[api_key]


__all__ = ["DotaMarketClientFactory"]

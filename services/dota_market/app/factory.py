from ..infra.rate_limiter import RateLimiterRegistry
from ..infra.client import DotaMarketClient
from ..infra.client.protocols import IAsyncHTTPSession
from .gateway import DotaMarketGateway


class DotaMarketFactory:

    BASE_URL = "https://market.dota2.net/api/"
    DEFAULT_RPS = 5

    _limiter_registry = RateLimiterRegistry(default_rps=DEFAULT_RPS)

    @classmethod
    def get(cls, api_key: str, session: IAsyncHTTPSession) -> DotaMarketGateway:
        client = DotaMarketClient(
            api_key=api_key, base_url=cls.BASE_URL, session=session
        )
        return DotaMarketGateway(
            client=client, rate_limiter=cls._limiter_registry.get(api_key)
        )

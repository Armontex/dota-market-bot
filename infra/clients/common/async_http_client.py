from httpx import AsyncClient, Response
from httpx import HTTPStatusError, RequestError
from common.logger import logger
from .enums import RequestMethod


class AsyncHTTPClient:

    DEFAULT_TIMEOUT = 5  # Seconds

    def __init__(self, base_url: str, **kwargs) -> None:
        self._base_url = base_url
        self._kwargs = kwargs
        self._client: AsyncClient | None = None

        kwargs.setdefault("timeout", self.DEFAULT_TIMEOUT)

    async def get(self, url: str, **kwargs) -> Response:
        return await self._request(RequestMethod.GET, url, **kwargs)

    async def post(self, url: str, **kwargs) -> Response:
        return await self._request(RequestMethod.POST, url, **kwargs)

    async def put(self, url: str, **kwargs) -> Response:
        return await self._request(RequestMethod.PUT, url, **kwargs)

    async def delete(self, url: str, **kwargs) -> Response:
        return await self._request(RequestMethod.DELETE, url, **kwargs)

    async def patch(self, url: str, **kwargs) -> Response:
        return await self._request(RequestMethod.PATCH, url, **kwargs)

    async def _request(self, method: str, url: str, **kwargs) -> Response:
        if not self._client:
            raise RuntimeError("HTTP client не инициализирован.")
        try:
            logger.bind(method=method, url=url, kwargs=kwargs).debug(
                f"Отправка запроса."
            )
            response = await self._client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except HTTPStatusError as e:
            logger.bind(method=method, url=url).error(
                f"HTTP ошибка: {e.response.status_code}"
            )
            raise
        except RequestError as e:
            logger.bind(method=method, url=url, kwargs=kwargs).error(
                f"Ошибка запроса: {str(e)}"
            )
            raise

    async def __aenter__(self):
        self._client = AsyncClient(base_url=self._base_url, **self._kwargs)
        return self

    async def __aexit__(self, *args):
        if self._client:
            await self._client.aclose()

from httpx import AsyncClient, Response
from httpx import HTTPStatusError, RequestError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from common.logger import logger
from .enums import RequestMethod


class AsyncHTTPSession:

    DEFAULT_TIMEOUT = 5  # Seconds

    def __init__(self, base_url: str = "", **kwargs) -> None:
        self._base_url = base_url
        self._kwargs = kwargs
        self._client: AsyncClient | None = None

        kwargs.setdefault("timeout", self.DEFAULT_TIMEOUT)

    async def get(self, endpoint: str, **kwargs) -> Response:
        return await self.request(RequestMethod.GET, endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> Response:
        return await self.request(RequestMethod.POST, endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs) -> Response:
        return await self.request(RequestMethod.PUT, endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs) -> Response:
        return await self.request(RequestMethod.DELETE, endpoint, **kwargs)

    async def patch(self, endpoint: str, **kwargs) -> Response:
        return await self.request(RequestMethod.PATCH, endpoint, **kwargs)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((HTTPStatusError, RequestError)),
        reraise=True,
    )
    async def request(self, method: str, endpoint: str, **kwargs) -> Response:
        if not self._client:
            raise RuntimeError("HTTP client не инициализирован.")
        try:
            logger.bind(method=method, endpoint=endpoint, kwargs=kwargs).debug(
                f"Отправка запроса."
            )
            response = await self._client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response
        except HTTPStatusError as e:
            logger.bind(method=method, endpoint=endpoint).error(
                f"HTTP ошибка: {e.response.status_code}"
            )
            raise
        except RequestError as e:
            logger.bind(method=method, endpoint=endpoint, kwargs=kwargs).error(
                f"Ошибка запроса: {str(e)}"
            )
            raise

    async def __aenter__(self):
        self._client = AsyncClient(base_url=self._base_url, **self._kwargs)
        return self

    async def __aexit__(self, *args):
        if self._client:
            await self._client.aclose()

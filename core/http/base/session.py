from abc import ABC, abstractmethod
from typing import Literal

HTTPRequest = Literal["GET", "POST", "DELETE", "PATCH", "PUT"]


class BaseAsyncSession[TResponse](ABC):

    @abstractmethod
    async def request(self, method: HTTPRequest, endpoint: str, **kwargs) -> TResponse:
        pass

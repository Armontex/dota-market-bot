from typing import Protocol, Literal, Any

HTTPRequest = Literal["GET", "POST", "DELETE", "PATCH", "PUT"]


class IResponse(Protocol):

    def json(self, *args, **kwargs) -> dict[str, Any]: ...


class IAsyncHTTPSession(Protocol):

    async def request(
        self, method: HTTPRequest, endpoint: str, **kwargs
    ) -> IResponse: ...

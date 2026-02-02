import pytest
from unittest.mock import AsyncMock, patch
from httpx import Response, Request, HTTPStatusError, RequestError
from infra.clients.common.async_http_session import AsyncHTTPSession
from infra.clients.common.enums import RequestMethod


@pytest.fixture
def session():
    return AsyncHTTPSession(base_url="https://example.com")


async def test_context_manager_creates_and_closes_client(session):
    with patch("infra.clients.common.async_http_session.AsyncClient") as client_cls:
        client_instance = AsyncMock()
        client_cls.return_value = client_instance

        async with session as s:
            assert s._client is client_instance

        client_instance.aclose.assert_awaited_once()


async def test_request_without_client_raises():
    session = AsyncHTTPSession()

    with pytest.raises(RuntimeError):
        await session.get("/test")


@pytest.mark.parametrize(
    "method,func",
    [
        (RequestMethod.GET, "get"),
        (RequestMethod.POST, "post"),
        (RequestMethod.PUT, "put"),
        (RequestMethod.DELETE, "delete"),
        (RequestMethod.PATCH, "patch"),
    ],
)
async def test_http_methods_delegate_to_request(session, method, func):
    session.request = AsyncMock()

    await getattr(session, func)("/endpoint", json={"a": 1})

    session.request.assert_awaited_once_with(method, "/endpoint", json={"a": 1})


async def test_successful_request_returns_response(session):
    response = Response(
        status_code=200,
        request=Request("GET", "https://example.com/test"),
    )

    async with session:
        session._client.request = AsyncMock(return_value=response)

        result = await session.get("/test")

        assert result is response
        session._client.request.assert_awaited_once()


async def test_http_status_error_retried_3_times(session):
    request = Request("GET", "https://example.com/test")
    response = Response(status_code=500, request=request)

    error = HTTPStatusError(
        message="error",
        request=request,
        response=response,
    )

    async with session:
        session._client.request = AsyncMock(return_value=response)

        with patch.object(Response, "raise_for_status", side_effect=error):
            with pytest.raises(HTTPStatusError):
                await session.get("/test")

        assert session._client.request.await_count == 3


async def test_request_error_retried_3_times(session):
    async with session:
        session._client.request = AsyncMock(side_effect=RequestError("network error"))

        with pytest.raises(RequestError):
            await session.get("/test")

        assert session._client.request.await_count == 3


async def test_non_retryable_exception_not_retried(session):
    async with session:
        session._client.request = AsyncMock(side_effect=ValueError("bug"))

        with pytest.raises(ValueError):
            await session.get("/test")

        assert session._client.request.await_count == 1


async def test_retry_then_success(session):
    request = Request("GET", "https://example.com/test")
    response = Response(status_code=200, request=request)

    async def side_effect(*args, **kwargs):
        if side_effect.calls < 2:
            side_effect.calls += 1
            raise RequestError("temporary error")
        return response

    side_effect.calls = 0

    async with session:
        session._client.request = AsyncMock(side_effect=side_effect)

        result = await session.get("/test")

        assert result is response
        assert session._client.request.await_count == 3


@pytest.mark.asyncio
async def test_async_client_created_with_base_url_and_kwargs():
    with patch("infra.clients.common.async_http_session.AsyncClient") as client_cls:
        client_instance = AsyncMock()
        client_cls.return_value = client_instance

        session = AsyncHTTPSession(
            base_url="https://api.test",
            timeout=10,
        )

        async with session:
            pass

        client_cls.assert_called_once_with(
            base_url="https://api.test",
            timeout=10,
        )

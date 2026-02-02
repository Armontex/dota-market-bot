import pytest
from unittest.mock import AsyncMock
from pydantic import ValidationError, BaseModel
from infra.clients.common.decorators import handle_api_errors, limit_rate


class TestModel(BaseModel):
    x: int


async def test_handle_api_errors_validation_error():

    @handle_api_errors
    async def fn():
        TestModel(x="boom")  # type: ignore

    with pytest.raises(ValidationError):
        await fn()


async def test_handle_api_errors_exception_error():

    @handle_api_errors
    async def fn():
        raise

    with pytest.raises(Exception):
        await fn()


async def test_limit_rate_has_limiter():
    limiter = AsyncMock()
    wait = AsyncMock()
    limiter.wait = wait

    class Obj:
        def __init__(self):
            self._rate_limiter = limiter

        @limit_rate()
        async def fn(self):
            return "ok"

    obj = Obj()

    result = await obj.fn()

    limiter.wait.assert_awaited_once()
    assert result == "ok"


async def test_limit_rate_with_different_name_without_arg():
    limiter = AsyncMock()
    wait = AsyncMock()
    limiter.wait = wait

    class Obj:
        def __init__(self):
            self._some_name = limiter

        @limit_rate()
        async def fn(self):
            return "ok"

    obj = Obj()

    result = await obj.fn()

    wait.assert_not_awaited()
    assert result == "ok"


async def test_limit_rate_with_different_name():
    limiter = AsyncMock()
    wait = AsyncMock()
    limiter.wait = wait

    class Obj:
        def __init__(self):
            self._some_name = limiter

        @limit_rate(rate_limiter_attr="_some_name")
        async def fn(self):
            return "ok"

    obj = Obj()

    result = await obj.fn()

    wait.assert_awaited_once()
    assert result == "ok"

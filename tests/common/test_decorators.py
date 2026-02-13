import pytest
from typing import Any
from pydantic import BaseModel, ValidationError
from unittest.mock import AsyncMock


# ==== abstract_pydantic_model ====
from common.decorators import abstract_model


@pytest.fixture
def abstract_model():
    @abstract_model
    class AbstractModel(BaseModel):
        field: Any

    return AbstractModel


def test_abstract_pydantic_model(abstract_model):
    "Проверка, что абстрактная модель не может быть проинициализированна"
    with pytest.raises(TypeError):
        abstract_model(field=123)


def test_abstract_pydantic_model_subclass(abstract_model):
    "Проверка, что наследник абстрактной модели может инициализироваться"

    class A(abstract_model): ...

    a = A(field=123)

    assert a.field == 123


# ==== handle_api_errors ====
from common.decorators import handle_api_errors


class TestModel(BaseModel):
    x: int


async def test_handle_api_errors_validation_error():
    "Проверка, что обрабатывается ошибка валидации"

    @handle_api_errors
    async def fn():
        TestModel(x="boom")  # type: ignore

    with pytest.raises(ValidationError):
        await fn()


async def test_handle_api_errors_exception_error():
    "Проверка, что прочие ошибки обрабатываются"

    @handle_api_errors
    async def fn():
        raise

    with pytest.raises(Exception):
        await fn()


# ==== limit_rate_method ====
from common.decorators import _is_rate_limiter, limit_rate_method


def test_valid_rate_limiter():
    """Проверка, что объект с async wait() распознается как rate limiter"""

    class ValidLimiter:
        async def wait(self):
            pass

    limiter = ValidLimiter()
    assert _is_rate_limiter(limiter) is True


def test_sync_wait_method():
    """Проверка, что синхронный wait() не считается rate limiter"""

    class SyncWaitLimiter:
        def wait(self):
            pass

    limiter = SyncWaitLimiter()
    assert _is_rate_limiter(limiter) is False


def test_no_wait_method():
    """Проверка объекта без метода wait()"""

    class NoWaitLimiter:
        pass

    limiter = NoWaitLimiter()
    assert _is_rate_limiter(limiter) is False


def test_none_object():
    """Проверка None"""
    assert _is_rate_limiter(None) is False


def test_wait_is_not_callable():
    """Проверка, когда wait не является вызываемым"""

    class BadLimiter:
        wait = "not a function"

    limiter = BadLimiter()
    assert _is_rate_limiter(limiter) is False


async def test_successful_rate_limiting():
    """Тест успешного вызова с rate limiter"""

    mock_limiter = AsyncMock()

    class MyClass:
        def __init__(self):
            self._rate_limiter = mock_limiter

        @limit_rate_method()
        async def my_method(self, value):
            return value * 2

    obj = MyClass()
    result = await obj.my_method(5)

    mock_limiter.wait.assert_awaited_once()

    assert result == 10


async def test_custom_rate_limiter_attribute():
    """Тест с кастомным именем атрибута rate limiter"""
    mock_limiter = AsyncMock()

    class MyClass:
        def __init__(self):
            self.custom_limiter = mock_limiter

        @limit_rate_method(rate_limiter_attr="custom_limiter")
        async def my_method(self):
            return "success"

    obj = MyClass()
    result = await obj.my_method()

    mock_limiter.wait.assert_awaited_once()
    assert result == "success"


async def test_missing_rate_limiter():
    """Тест ошибки при отсутствии rate limiter"""

    class MyClass:
        @limit_rate_method()
        async def my_method(self):
            return "should not reach"

    obj = MyClass()

    with pytest.raises(TypeError, match="не реализует IRateLimiter"):
        await obj.my_method()


async def test_invalid_rate_limiter_sync_wait():
    """Тест ошибки при синхронном wait()"""

    class SyncLimiter:
        def wait(self):
            pass

    class MyClass:
        def __init__(self):
            self._rate_limiter = SyncLimiter()

        @limit_rate_method()
        async def my_method(self):
            return "should not reach"

    obj = MyClass()

    with pytest.raises(TypeError, match="не реализует IRateLimiter"):
        await obj.my_method()


async def test_method_with_args_and_kwargs():
    """Тест передачи аргументов и kwargs в метод"""
    mock_limiter = AsyncMock()

    class MyClass:
        def __init__(self):
            self._rate_limiter = mock_limiter

        @limit_rate_method()
        async def my_method(self, a, b, c=None):
            return (a, b, c)

    obj = MyClass()
    result = await obj.my_method(1, 2, c="test")

    mock_limiter.wait.assert_awaited_once()
    assert result == (1, 2, "test")


async def test_multiple_calls():
    """Тест множественных вызовов метода"""
    mock_limiter = AsyncMock()

    class MyClass:
        def __init__(self):
            self._rate_limiter = mock_limiter

        @limit_rate_method()
        async def my_method(self):
            return "ok"

    obj = MyClass()

    await obj.my_method()
    await obj.my_method()
    await obj.my_method()

    # Проверяем, что wait был вызван 3 раза
    assert mock_limiter.wait.await_count == 3


async def test_exception_in_decorated_method():
    """Тест, что исключения пробрасываются из декорированного метода"""
    mock_limiter = AsyncMock()

    class MyClass:
        def __init__(self):
            self._rate_limiter = mock_limiter

        @limit_rate_method()
        async def my_method(self):
            raise ValueError("Test exception")

    obj = MyClass()

    with pytest.raises(ValueError, match="Test exception"):
        await obj.my_method()

    mock_limiter.wait.assert_awaited_once()


async def test_wraps_preserves_metadata():
    """Тест, что декоратор сохраняет метаданные функции"""

    class MyClass:
        @limit_rate_method()
        async def my_method(self):
            """This is a docstring"""
            pass

    assert MyClass.my_method.__name__ == "my_method"
    assert MyClass.my_method.__doc__ == "This is a docstring"

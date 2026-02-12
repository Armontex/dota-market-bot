import warnings
import inspect
from typing import Protocol, TypeGuard, Any
from functools import wraps
from pydantic import ValidationError
from .logger import logger


def abstract_pydantic_model[T: type](cls: T) -> T:
    """Декоратор, запрещающий создание экземпляров декорируемого класса."""
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        if type(self) is cls:
            raise TypeError(f"{cls.__name__} is abstract and cannot be instantiated")
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls


def emit_runtime_warning[T: type](cls: T) -> T:
    """
    Берет сообщение из атрибута __deprecated__, который ставит @deprecated,
    и добавляет warning в __init__.
    """
    message = getattr(cls, "__deprecated__", None)

    if message is None:
        message = f"{cls.__name__} is deprecated."

    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        warnings.warn(message, category=DeprecationWarning, stacklevel=2)
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls


def handle_api_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValidationError as e:
            logger.bind(func_name=func.__name__, error=e.json()).error(
                f"Ошибка валидации Pydantic"
            )
            raise
        except Exception as e:
            logger.bind(func_name=func.__name__, str=str(e)).error(
                "Непредвиденная ошибка"
            )
            raise

    return wrapper


class _IRateLimiter(Protocol):
    async def wait(self) -> None: ...


def _is_rate_limiter(obj: Any) -> TypeGuard[_IRateLimiter]:
    wait = getattr(obj, "wait", None)
    return bool(wait) and inspect.iscoroutinefunction(wait)


def limit_rate_method(rate_limiter_attr: str = "_rate_limiter"):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            limiter = getattr(self, rate_limiter_attr, None)
            if not _is_rate_limiter(limiter):
                raise TypeError(f"{limiter} не реализует IRateLimiter")
            await limiter.wait()

            return await func(self, *args, **kwargs)

        return wrapper

    return decorator

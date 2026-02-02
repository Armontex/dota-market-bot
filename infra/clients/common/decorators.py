from functools import wraps
from pydantic import ValidationError
from common.logger import logger


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


def limit_rate(rate_limiter_attr: str = "_rate_limiter"):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            limiter = getattr(self, rate_limiter_attr, None)
            if limiter and callable(getattr(limiter, "wait", None)):
                await limiter.wait()
            return await func(self, *args, **kwargs)

        return wrapper

    return decorator

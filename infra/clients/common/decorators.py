import functools
from pydantic import ValidationError
from common.logger import logger


def handle_api_errors(func):

    @functools.wraps(func)
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

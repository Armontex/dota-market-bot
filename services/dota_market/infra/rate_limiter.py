import asyncio
import time
from typing import Any


class RateLimiter:
    """Этот класс RateLimiter реализует ограничение частоты запросов с заданной частотой в секунду и
    функцию ожидания определенного интервала времени перед выполнением следующей операции.
    """

    def __init__(self, rps: int) -> None:
        """Этот метод инициализирует объект с заданной частотой запросов в секунду (rps).

        Parameters
        ----------
        rps : int
            Конструктор класса принимает аргумент rps, который представляет собой количество запросов в
        секунду (requests per second). Этот аргумент используется для вычисления интервала между
        запросами

        """
        self._interval = 1 / rps
        self._last_used = 0.0
        self._lock = asyncio.Lock()

    async def wait(self) -> None:
        """Функция `wait` выполняет ожидание определенного интервала времени перед выполнением следующей
        операции.
        """
        async with self._lock:
            now = time.perf_counter()
            wait = self._interval - (now - self._last_used)
            if wait > 0:
                await asyncio.sleep(wait)
            self._last_used = time.perf_counter()


class RateLimiterRegistry:
    """
    Класс RateLimiterRegistry представляет собой реестр ограничителей частоты запросов, который
    позволяет получать объекты RateLimiter по ключу и создавать новые, если ключ отсутствует.
    """

    def __init__(self, default_rps: int) -> None:
        """Этот метод инициализирует объект с заданным значением default_rps и пустым словарем для хранения
        ограничителей скорости.

        Parameters
        ----------
        default_rps : int
            Конструктор класса принимает параметр default_rps, который представляет собой количество
        запросов в секунду по умолчанию.
        """
        self._default_rps = default_rps
        self._limiters: dict[Any, RateLimiter] = {}

    def get(self, key: Any) -> RateLimiter:
        """Эта функция возвращает объект RateLimiter для указанного ключа, создавая новый, если ключ
        отсутствует.

        Parameters
        ----------
        key : Any
            Ключ, который используется для получения объекта RateLimiter из словаря self._limiters.

        Returns
        -------
            Возвращается объект RateLimiter, связанный с указанным ключом. Если объект RateLimiter не
        существует для данного ключа, то создается новый объект с заданным значением rps (запросов в
        секунду) и сохраняется в словаре self._limiters.
        """
        if key not in self._limiters:
            self._limiters[key] = RateLimiter(self._default_rps)
        return self._limiters[key]

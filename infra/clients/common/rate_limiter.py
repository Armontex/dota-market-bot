import asyncio
import time
from typing import Any


class RateLimiter:

    def __init__(self, rps: int) -> None:
        self._interval = 1 / rps
        self._last_used = 0.0
        self._lock = asyncio.Lock()

    async def wait(self) -> None:
        """
        The `wait` function asynchronously waits for a specified interval before updating the last used
        time.
        """
        async with self._lock:
            now = time.perf_counter()
            wait = self._interval - (now - self._last_used)
            if wait > 0:
                await asyncio.sleep(wait)
            self._last_used = time.perf_counter()


class RateLimiterRegistry:

    def __init__(self, default_rps: int) -> None:
        self._default_rps = default_rps
        self._limiters: dict[Any, RateLimiter] = {}

    def get(self, key: Any) -> RateLimiter:
        if key not in self._limiters:
            self._limiters[key] = RateLimiter(self._default_rps)
        return self._limiters[key]

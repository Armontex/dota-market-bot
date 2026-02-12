import time
import random
from services.dota_market.infra.rate_limiter import RateLimiter


async def test_rate_limiter_wait():

    async def some_method(limiter: RateLimiter) -> float:
        await limiter.wait()
        return time.perf_counter()

    rps = 5
    interval = 1 / rps
    limiter = RateLimiter(rps)

    times = []
    for _ in range(random.randint(5, 15)):
        times.append(await some_method(limiter))

    for prev, curr in zip(times, times[1:]):
        assert curr - prev >= interval

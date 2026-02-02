from typing import Protocol


class IRateLimiter(Protocol):

    async def wait(self) -> None: ...

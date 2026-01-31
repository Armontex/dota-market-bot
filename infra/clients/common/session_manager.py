import asyncio
import time
from .async_http_client import AsyncHTTPClient


class SessionManager:

    TTL = 20 * 60  # 20 минут
    CLEANUP_INTERVAL = 5 * 60  # каждые 5 минут

    def __init__(self) -> None:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            raise RuntimeError(
                "SessionManager должен создаваться внутри запущенного event loop"
            )

        self._sessions: dict[str, tuple[AsyncHTTPClient, float]] = {}
        self._cleanup_task = asyncio.create_task(self._cleanup_sessions())

    async def get_session(self, key, base_url: str, **kwargs) -> AsyncHTTPClient:
        """
        Retrieve or create an asynchronous HTTP client session associated with the given key.
        If a session for the specified key already exists, it is reused. Otherwise, a new
        AsyncHTTPClient is created, initialized, and stored for future use.
        
        :param key: Unique identifier for the session.
        :param base_url: The base URL for the HTTP client.
        :param kwargs: Additional keyword arguments to pass to the AsyncHTTPClient constructor.
        :return: An instance of AsyncHTTPClient associated with the given key.
        :rtype: AsyncHTTPClient
        """
        now = time.perf_counter()

        if key in self._sessions:
            client, _ = self._sessions[key]
        else:
            client = AsyncHTTPClient(base_url, **kwargs)
            await client.__aenter__()
        self._sessions[key] = (client, now)
        return client

    async def _cleanup_sessions(self) -> None:
        """
        Periodically cleans up expired sessions from the session manager.

        This asynchronous method runs in an infinite loop, sleeping for a predefined interval
        (`CLEANUP_INTERVAL`) between iterations. On each iteration, it checks all managed sessions
        and removes those that have not been used for longer than the time-to-live (`TTL`).
        For each expired session, it calls the asynchronous exit method (`__aexit__`) on the client
        before removing it from the session storage.
        """
        while True:
            await asyncio.sleep(self.CLEANUP_INTERVAL)
            now = time.perf_counter()
            for key, (client, last_used) in self._sessions.items():
                if now - last_used > self.TTL:
                    await client.__aexit__()
                    self._sessions.pop(key)


__all__ = ["SessionManager"]
from ..base import AsyncSMTPClient


class AsyncGmailSMTPAdapter(AsyncSMTPClient):

    def __init__(self, *, login: str, app_password: str) -> None:
        super().__init__(
            host_name="smtp.gmail.com",
            port=465,
            login=login,
            password=app_password,
            use_tls=True,
        )

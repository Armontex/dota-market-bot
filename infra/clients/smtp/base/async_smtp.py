from typing import Literal, Self
from aiosmtplib import SMTP, SMTPResponse, SMTPRecipientsRefused, SMTPResponseException
from email.message import EmailMessage
from common.logger import logger
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


Response = tuple[dict[str, SMTPResponse], str]


class AsyncSMTPClient:

    def __init__(
        self,
        host_name: str,
        port: Literal[465, 587] | int,
        *,
        login: str,
        password: str,
        **kwargs,
    ) -> None:
        self._smtp = SMTP(
            hostname=host_name, port=port, username=login, password=password, **kwargs
        )

    async def __aenter__(self) -> Self:
        await self._smtp.connect()
        return self

    async def __aexit__(self, *args) -> None:
        await self._smtp.quit()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((SMTPRecipientsRefused, Exception)),
        reraise=True,
    )
    async def send_message(
        self,
        message: EmailMessage,
        /,
        **kwargs,
    ) -> Response:
        if not self._smtp.is_connected:
            raise RuntimeError("Воспользуйте контекстным менеджером для подключения.")

        bounded_logger = logger.bind(
            sender=message["From"],
            recipients=message["To"],
            host=self._smtp.hostname,
            port=self._smtp.port,
        )
        try:
            bounded_logger.debug("Отправка сообщений")
            return await self._smtp.send_message(message, **kwargs)
        except ValueError:
            bounded_logger.error("Неправильно заполнен `EmailMessage`")
            raise
        except SMTPRecipientsRefused:
            bounded_logger.error("Доставка всем получателям провалилась")
            raise
        except SMTPResponseException:
            bounded_logger.error("Неверный запрос")
            raise
        except Exception as e:
            bounded_logger.error(f"Непредвиденная ошибка: {str(e)}")
            raise

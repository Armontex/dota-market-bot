from ..base import BaseNotifier
from ..base.dto import DTO, BaseMessage, BaseNotificationLog
from typing import TypeAlias, Literal
from pydantic import Field
from common.logger import logger


TelegramSender: TypeAlias = Literal["bot"]
TelegramRecipient: TypeAlias = int


class TextContent(DTO):
    text: str = Field(min_length=1, description="Текст сообщения")


class PhotoContent(DTO):
    photo: bytes = Field(min_length=1, description="Фотография")
    caption: str | None = Field(..., description="Текст под фото")


TelegramContent: TypeAlias = TextContent | PhotoContent
TelegramMessage: TypeAlias = BaseMessage[
    TelegramSender, TelegramRecipient, TelegramContent
]
TelegramNotificationLog: TypeAlias = BaseNotificationLog[
    TelegramSender, TelegramRecipient
]


class TelegramNotifier(
    BaseNotifier[TelegramSender, TelegramRecipient, TelegramContent]
):

    async def send(self, message: TelegramMessage) -> TelegramNotificationLog:
        logger.bind(
            sender=message.sender, recipient=message.recipient, title=message.title
        ).debug("Отправка уведомления через телеграм")
        return await self._send_content(message)

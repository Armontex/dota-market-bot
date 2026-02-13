from typing import Literal
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession
from common.pydantic import DTO
from ..base import BaseMessage, BaseMessageMeta, BaseNotifier, IMessageSender, Log
from ...common.enums import NotificationChannel


class TextContent(DTO):
    text: str = Field(min_length=1, description="Текст сообщения")


class PhotoContent(DTO):
    photo: bytes = Field(min_length=1, description="Фотография")
    caption: str | None = Field(
        default=None, min_length=1, description="Текст под фото"
    )


Bot = Literal["bot"]
ChatID = int
TelegramMessageContent = TextContent | PhotoContent

TelegramMessageMeta = BaseMessageMeta[Bot, ChatID]
TelegramMessage = BaseMessage[TelegramMessageMeta, TelegramMessageContent]
ITelegramSender = IMessageSender[TelegramMessage]


# NOTESTED
class TelegramNotifier(BaseNotifier[TelegramMessage]):

    def __init__(self, sender: ITelegramSender, session: AsyncSession) -> None:
        super().__init__(sender, session)

    def _get_service_name(self) -> NotificationChannel:
        return NotificationChannel.TELEGRAM

    async def send(
        self, chat_id: ChatID, title: str, content: TelegramMessageContent
    ) -> Log[TelegramMessage]:
        meta = TelegramMessageMeta(sender="bot", recipient=chat_id, title=title)
        message = TelegramMessage(meta=meta, content=content)
        return await super().send(message)

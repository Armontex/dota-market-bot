from typing import Literal
from pydantic import Field
from core.base.dto import DTO
from ..base.protocols import INotifyGateway
from ..base import BaseNotifier
from ..base.dto import BaseMessage, MessageMeta


class TextContent(DTO):
    text: str = Field(min_length=1, description="Текст сообщения")


class PhotoContent(DTO):
    photo: bytes = Field(min_length=1, description="Фотография")
    caption: str | None = Field(..., min_length=1, description="Текст под фото")


Bot = Literal["bot"]
ChatID = int
MessageContent = TextContent | PhotoContent

TelegramMessageMeta = MessageMeta[Bot, ChatID]
TelegramMessage = BaseMessage[TelegramMessageMeta, MessageContent]
ITelegramGateway = INotifyGateway[TelegramMessage]


class TelegramNotifier(BaseNotifier[TelegramMessage]):

    @property
    def SERVICE_NAME(self) -> str:
        return "Telegram"

    async def send(self, chat_id: ChatID, title: str, content: MessageContent):
        meta = TelegramMessageMeta(sender="bot", recipient=chat_id, title=title)
        message = TelegramMessage(meta=meta, content=content)
        return await self._send_message(message)

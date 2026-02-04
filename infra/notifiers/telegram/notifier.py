from typing import Literal
from pydantic import Field
from core.base.dto import DTO
from ..base.protocols import INotifyGateway
from ..base import BaseNotifier, NotificationLog
from ..base.dto import BaseMessage, BaseMessageMeta


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
ITelegramGateway = INotifyGateway[TelegramMessage]


class TelegramNotifier(BaseNotifier[TelegramMessage]):

    def _get_service_name(self) -> str:
        return "Telegram"

    async def send(
        self, chat_id: ChatID, title: str, content: TelegramMessageContent
    ) -> NotificationLog[TelegramMessage]:
        meta = TelegramMessageMeta(sender="bot", recipient=chat_id, title=title)
        message = TelegramMessage(meta=meta, content=content)
        return await self._send_message(message)

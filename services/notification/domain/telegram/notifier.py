from typing import Literal
from pydantic import Field
from common.pydantic_models import DTO
from ..base.protocols import IMessageSender
from ..base.notifier import BaseNotifier
from ..base.models import BaseMessage, BaseMessageMeta, NotificationLog


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
ITelegramGateway = IMessageSender[TelegramMessage]


# NOTESTED
class TelegramNotifier(BaseNotifier[TelegramMessage]):

    def _get_service_name(self) -> str:
        return "Telegram"

    async def send(
        self, chat_id: ChatID, title: str, content: TelegramMessageContent
    ) -> NotificationLog[TelegramMessage]:
        meta = TelegramMessageMeta(sender="bot", recipient=chat_id, title=title)
        message = TelegramMessage(meta=meta, content=content)
        return await super().send(message)

from typing import Literal
from pydantic import Field
from ..base.protocols import INotifyGateway
from ..base import BaseNotifier
from ..base.dto import DTO, BaseMessage, MessageMeta


class TextContent(DTO):
    text: str = Field(min_length=1, description="Текст сообщения")


class PhotoContent(DTO):
    photo: bytes = Field(min_length=1, description="Фотография")
    caption: str | None = Field(..., min_length=1, description="Текст под фото")


Bot = Literal["bot"]
ChatID = int

TelegramMessage = BaseMessage[MessageMeta[Bot, ChatID], TextContent | PhotoContent]
ITelegramGateway = INotifyGateway[TelegramMessage]


class TelegramNotifier(BaseNotifier[TelegramMessage]):

    @property
    def SERVICE_NAME(self) -> str:
        return "Telegram"

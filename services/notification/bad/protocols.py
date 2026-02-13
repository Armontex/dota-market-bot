from typing import Protocol
from .models import BaseMessage, Log
from ..common.enums import MessageStatus, NotificationChannel


class IMessageSender[TMessage: BaseMessage](Protocol):

    async def send_message(self, message: TMessage) -> MessageStatus: ...


class INotificationLogRepository[TMessage: BaseMessage](Protocol):
    async def create_notification(
        self, channel: NotificationChannel, log: Log[TMessage]
    ) -> None: ...

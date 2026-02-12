from typing import Protocol
from .models import BaseMessage
from .enums import MessageStatus


class IMessageSender[TMessage: BaseMessage](Protocol):

    async def send_message(self, message: TMessage) -> MessageStatus: ...

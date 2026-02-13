from typing import Protocol
from .models import BaseMessage
from ...common.enums import MessageStatus


class IMessageSender[TMessage: BaseMessage](Protocol):

    async def send_message(self, message: TMessage) -> MessageStatus: ...

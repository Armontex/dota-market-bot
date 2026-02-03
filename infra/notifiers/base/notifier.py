from typing import Generic, TypeVar
from abc import ABC, abstractmethod
from .dto.incoming import BaseMessage
from .dto.outgoing import BaseNotificationLog
from .protocols import INotifyGateway


TSender = TypeVar("TSender")
TRecipient = TypeVar("TRecipient")
TContent = TypeVar("TContent")


class BaseNotifier(Generic[TSender, TRecipient, TContent], ABC):

    def __init__(self, gateway: INotifyGateway[TSender, TRecipient, TContent]) -> None:
        self._gateway = gateway

    @abstractmethod
    async def send(
        self, message: BaseMessage[TSender, TRecipient, TContent]
    ) -> BaseNotificationLog[TSender, TRecipient]:
        raise NotImplementedError()

    async def _send_content(
        self, message: BaseMessage[TSender, TRecipient, TContent]
    ) -> BaseNotificationLog[TSender, TRecipient]:
        status = await self._gateway.send_content(
            sender=message.sender, recipient=message.recipient, content=message.content
        )
        return BaseNotificationLog(
            sender=message.sender,
            recipient=message.recipient,
            title=message.title,
            status=status,
        )

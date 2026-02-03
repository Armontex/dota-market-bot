from typing import Generic, TypeVar, Protocol
from http import HTTPStatus


TSender = TypeVar("TSender", contravariant=True)
TRecipient = TypeVar("TRecipient", contravariant=True)
TContent = TypeVar("TContent", contravariant=True)


class INotifyGateway(Generic[TSender, TRecipient, TContent], Protocol):

    async def send_content(
        self, sender: TSender, recipient: TRecipient, content: TContent
    ) -> HTTPStatus: ...

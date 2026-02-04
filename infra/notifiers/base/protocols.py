from typing import Protocol
from http import HTTPStatus
from .dto.incoming import BaseMessage


class INotifyGateway[TMessage: BaseMessage](Protocol):

    async def send_message(self, message: TMessage) -> HTTPStatus: ...

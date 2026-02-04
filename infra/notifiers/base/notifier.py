from abc import ABC, abstractmethod
from common.logger import logger
from .dto.incoming import BaseMessage
from .dto.outgoing import NotificationLog
from .protocols import INotifyGateway


class BaseNotifier[TMessage: BaseMessage](ABC):

    def __init__(self, gateway: INotifyGateway[TMessage]) -> None:
        self._gateway = gateway

    @property
    @abstractmethod
    def SERVICE_NAME(self) -> str:
        raise NotImplementedError()

    async def send(self, message: TMessage) -> NotificationLog[TMessage]:
        logger.bind(recipient=message.meta.recipient, title=message.meta.title).info(
            f"Отправка уведомления в {self.SERVICE_NAME}"
        )
        status = await self._gateway.send_message(message)
        return NotificationLog(message=message, status=status)

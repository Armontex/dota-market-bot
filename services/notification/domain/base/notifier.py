from abc import ABC, abstractmethod
from common.logger import logger
from .models import BaseMessage, NotificationLog
from .protocols import IMessageSender


# NOTESTED
class BaseNotifier[TMessage: BaseMessage](ABC):

    def __init__(self, sender: IMessageSender[TMessage]) -> None:
        self._sender = sender

    @abstractmethod
    def _get_service_name(self) -> str:
        raise NotImplementedError()

    async def send(self, message: TMessage) -> NotificationLog[TMessage]:
        logger.bind(recipient=message.meta.recipient, title=message.meta.title).info(
            f"Отправка уведомления в {self._get_service_name()}"
        )

        status = await self._sender.send_message(message)

        # TODO: создать запись в БД

        return NotificationLog(message=message, status=status)

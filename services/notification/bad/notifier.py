from abc import ABC, abstractmethod
from common.logger import logger
from .models import BaseMessage, Log
from .protocols import IMessageSender, INotificationLogRepository
from ..common.enums import NotificationChannel


# NOTESTED
class BaseNotifier[TMessage: BaseMessage](ABC):

    def __init__(
        self,
        sender: IMessageSender[TMessage],
        repo: INotificationLogRepository[TMessage],
    ) -> None:
        self._sender = sender
        self._notification_repo = repo

    @abstractmethod
    def _get_service_name(self) -> NotificationChannel:
        raise NotImplementedError()

    async def send(self, message: TMessage) -> Log[TMessage]:
        logger.bind(recipient=message.meta.recipient, title=message.meta.title).info(
            f"Отправка уведомления в {self._get_service_name().value}"
        )

        status = await self._sender.send_message(message)
        log = Log(message=message, status=status)

        await self._notification_repo.create_notification(self._get_service_name(), log)

        return log

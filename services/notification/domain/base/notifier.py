from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from common.logger import logger
from .models import BaseMessage, Log
from .protocols import IMessageSender
from ...common.enums import NotificationChannel
from ...infra.db.repos.notification_log import NotificationRepository


# NOTESTED
class BaseNotifier[TMessage: BaseMessage](ABC):

    def __init__(self, sender: IMessageSender[TMessage], session: AsyncSession) -> None:
        self._sender = sender
        self._notification_repo = NotificationRepository(session)

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

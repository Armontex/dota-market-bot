from typing import Callable
from services.notification.domain.base.models import Log
from services.notification.domain.smtp.notifier import SMTPMessage
from services.notification.domain.telegram.notifier import TelegramMessage
from ..models.notification_log import (
    EmailNotificationLog,
    NotificationLog,
    TelegramNotificationLog,
)
from services.notification.common.enums import NotificationChannel

# NOTESTED
class LogMapper:

    @classmethod
    def get_mapper(
        cls, channel: NotificationChannel
    ) -> Callable[[Log], NotificationLog]:
        match channel:
            case NotificationChannel.EMAIL:
                return cls.map_log_to_email_log
            case NotificationChannel.TELEGRAM:
                return cls.map_log_to_telegram_log
            case _:
                raise NotImplementedError(f"Неизвестный канал уведомлений: {channel}")

    @staticmethod
    def map_log_to_telegram_log(log: Log[TelegramMessage]) -> TelegramNotificationLog:
        return TelegramNotificationLog(
            title=log.message.meta.title,
            status=log.status,
            chat_id=log.message.meta.recipient,
        )

    @staticmethod
    def map_log_to_email_log(log: Log[SMTPMessage]) -> EmailNotificationLog:
        return EmailNotificationLog(
            title=log.message.meta.title,
            status=log.status,
            sender=log.message.meta.sender,
            recipient=log.message.meta.recipient,
        )

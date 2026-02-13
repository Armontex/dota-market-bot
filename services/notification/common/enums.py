from enum import Enum


class MessageStatus(Enum):
    OK = "ok"
    ERROR = "error"


class NotificationChannel(Enum):
    EMAIL = "email"
    TELEGRAM = "telegram"

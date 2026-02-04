from pydantic import Field
from http import HTTPStatus
from typing import final
from .incoming import BaseMessage
from .base import DTO


@final
class NotificationLog[TMessage: BaseMessage](DTO):
    message: TMessage
    status: HTTPStatus = Field(..., description="Статус-код отправки уведомления")

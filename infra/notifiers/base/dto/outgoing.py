from pydantic import Field
from http import HTTPStatus
from typing import final
from core.base.dto import DTO
from .incoming import BaseMessage


@final
class NotificationLog[TMessage: BaseMessage](DTO):
    message: TMessage
    status: HTTPStatus = Field(..., description="Статус-код отправки уведомления")

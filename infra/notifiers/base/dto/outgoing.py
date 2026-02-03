from typing import Generic, TypeVar
from pydantic import Field
from http import HTTPStatus
from .base import DTO
from .incoming import MessageMetaInfo

TSender = TypeVar("TSender")
TRecipient = TypeVar("TRecipient")


class BaseNotificationLog(
    Generic[TSender, TRecipient], MessageMetaInfo[TSender, TRecipient], DTO
):
    status: HTTPStatus = Field(..., description="Статус-код отправки уведомления")

from pydantic import Field, field_validator, ValidationInfo
from typing import final
from common.decorators import abstract_pydantic_model
from common.pydantic_models import DTO
from .enums import MessageStatus


# NOTESTED
@abstract_pydantic_model
class BaseMessageMeta[TSender: str | int, TRecipient: str | int](DTO):
    sender: TSender = Field(..., description="Отправитель")
    recipient: TRecipient = Field(..., description="Получатель")
    title: str = Field(
        ...,
        min_length=1,
        description="Заголовок сообщения (не входит в состав сообщения)",
    )

    @field_validator("sender", "recipient")
    def validate_is_not_none(cls, v, info: ValidationInfo):
        if isinstance(v, str) and not v:
            raise ValueError(f"{info.field_name} не может быть пустой строкой")
        return v


@abstract_pydantic_model
class BaseMessage[TMeta: BaseMessageMeta, TContent](DTO):
    meta: TMeta
    content: TContent = Field(..., description="Контент сообщения")


@final
class NotificationLog[TMessage: BaseMessage](DTO):
    message: TMessage
    status: MessageStatus = Field(..., description="Статус отправки уведомления")

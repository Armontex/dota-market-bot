from pydantic import Field, field_validator, ValidationInfo
from .base import DTO


Sender = str | int
Recipient = str | int


class MessageMeta[TSender: Sender, TRecipient: Recipient](DTO):
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


class BaseMessage[TMeta: MessageMeta, TContent](DTO):
    meta: TMeta
    content: TContent = Field(..., description="Контент сообщения")

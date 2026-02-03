from typing import Generic, TypeVar
from pydantic import Field, field_validator, ValidationInfo
from .base import DTO


TSender = TypeVar("TSender")
TRecipient = TypeVar("TRecipient")
TContent = TypeVar("TContent")


class MessageMetaInfo(Generic[TSender, TRecipient], DTO):
    sender: TSender = Field(..., description="Отправитель")
    recipient: TRecipient = Field(..., description="Получатель")
    title: str = Field(
        ...,
        min_length=1,
        description="Заголовок сообщения (не входит в состав сообщения)",
    )

    @field_validator("sender", "recipient")
    def validate_is_not_none(cls, v, info: ValidationInfo):
        if v is None:
            raise ValueError(f"{info.field_name} не может быть None")
        return v


class BaseMessage(
    Generic[TSender, TRecipient, TContent], MessageMetaInfo[TSender, TRecipient], DTO
):
    content: TContent = Field(..., description="Контент сообщения")

    @field_validator("content")
    def validate_content(cls, v):
        if v is None:
            raise ValueError(f"content не может быть None")
        return v

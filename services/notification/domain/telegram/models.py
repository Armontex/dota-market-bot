from dataclasses import dataclass, field
from typing import Literal
from ..models import BaseMessageMeta, BaseMessage
from ..exc import DomainValidationError
from ..utils import non_empty_str

Bot = Literal["bot"]


@dataclass(frozen=True)
class TextContent:
    text: str

    def __post_init__(self):
        self._validate_text()

    def _validate_text(self) -> None:
        if not non_empty_str(self.text):
            raise DomainValidationError("text", "cannot be empty")
        if len(self.text) > 4096:
            raise DomainValidationError("text", "too long (max 4096)")


@dataclass(frozen=True)
class PhotoContent:
    photo: bytes
    caption: str | None = None

    def __post_init__(self):
        self._validate_photo()
        self._validate_caption()

    def _validate_photo(self) -> None:
        if self.photo == b"":
            raise DomainValidationError("photo", "cannot be empty")

    def _validate_caption(self) -> None:
        if self.caption is not None:
            if not non_empty_str(self.caption):
                raise DomainValidationError("caption", "cannot be empty")
            if len(self.caption) > 1024:
                raise DomainValidationError("caption", "too long (max 1024)")


@dataclass(frozen=True)
class TelegramMessageMeta(BaseMessageMeta[Bot, int]):
    sender: Bot = field(default="bot", init=False)

    def _validate_specific(self) -> None:
        if self.recipient <= 0:
            raise DomainValidationError("recipient", "must be > 0")


@dataclass(frozen=True)
class TelegramMessage(BaseMessage[TelegramMessageMeta, TextContent | PhotoContent]):

    def _validate_specific(self) -> None:
        pass

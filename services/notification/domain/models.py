from dataclasses import dataclass
from abc import ABC, abstractmethod
from .utils import non_empty_str
from ..common.enums import MessageStatus
from .exc import DomainValidationError


@dataclass(frozen=True)
class BaseMessageMeta[TSender, TRecipient](ABC):
    sender: TSender
    recipient: TRecipient
    title: str

    def __post_init__(self):
        self._title_validator()
        self._validate_specific()

    def _title_validator(self) -> None:
        if not non_empty_str(self.title):
            raise DomainValidationError("title", "cannot be empty")
        if len(self.title) > 150:
            raise DomainValidationError("title", "too long (max 150)")

    @abstractmethod
    def _validate_specific(self) -> None:
        pass


@dataclass(frozen=True)
class BaseMessage[TMeta: BaseMessageMeta, TContent](ABC):
    meta: TMeta
    content: TContent

    def __post_init__(self) -> None:
        self._validate_specific()

    @abstractmethod
    def _validate_specific(self) -> None:
        pass


@dataclass(frozen=True)
class Log[TMessage: BaseMessage]:
    message: TMessage
    status: MessageStatus

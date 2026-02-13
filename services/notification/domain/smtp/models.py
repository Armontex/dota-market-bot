from ..models import BaseMessage, BaseMessageMeta
from ..exc import DomainValidationError
from ..utils import validate_optional_string
from email_validator import validate_email, EmailNotValidError
from dataclasses import dataclass


@dataclass(frozen=True)
class EmailAddress:
    value: str

    def __post_init__(self):
        try:
            res = validate_email(self.value, check_deliverability=False)
        except EmailNotValidError as e:
            raise DomainValidationError("email", str(e)) from None
        object.__setattr__(self, "value", res.normalized)


@dataclass(frozen=True)
class SMTPMessageMeta(BaseMessageMeta[EmailAddress, EmailAddress]):

    def _validate_specific(self) -> None:
        pass


@dataclass(frozen=True)
class SMTPContent:
    text: str | None
    html: str | None

    def __post_init__(self):
        self._validate_content()
        self._validate_text()
        self._validate_html()

    def _validate_text(self) -> None:
        validate_optional_string("text", self.text)

    def _validate_html(self) -> None:
        validate_optional_string("html", self.html)

    def _validate_content(self) -> None:
        if not (self.text or self.html):
            raise DomainValidationError("content", "either text or html must be set")


@dataclass(frozen=True)
class SMTPMessage(BaseMessage[SMTPMessageMeta, SMTPContent]):

    def _validate_specific(self) -> None:
        pass

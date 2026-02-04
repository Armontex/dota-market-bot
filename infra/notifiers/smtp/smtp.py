from pydantic import EmailStr
from datetime import datetime, UTC
from email.message import EmailMessage as _EmailMessage
from email.utils import format_datetime
from email.policy import Policy
from ..base.dto.outgoing import NotificationLog
from ..base.protocols import INotifyGateway
from ..base import BaseNotifier
from ..base.dto import BaseMessage, BaseMessageMeta


class EmailMessage(_EmailMessage):
    def __init__(
        self,
        sender: EmailStr,
        recipient: EmailStr,
        *,
        subject: str | None = None,
        date: datetime = datetime.now(UTC),
        policy: Policy | None = None,
    ) -> None:
        super().__init__(policy=policy)

        self["From"] = str(sender)
        self["To"] = str(recipient)

        if subject:
            self["Subject"] = subject

        self["Date"] = format_datetime(date)


SMTPMessageMeta = BaseMessageMeta[EmailStr, EmailStr]
SMTPMessage = BaseMessage[SMTPMessageMeta, EmailMessage]
SMTPGateway = INotifyGateway[SMTPMessage]


class SMTPNotifier(BaseNotifier[SMTPMessage]):

    def _get_service_name(self) -> str:
        return "SMTP"

    async def send(self, message: EmailMessage) -> NotificationLog[SMTPMessage]:
        meta = SMTPMessageMeta(
            sender=message["From"],
            recipient=message["To"],
            title=message["Subject"] if message["Subject"] else "email message",
        )
        msg = SMTPMessage(meta=meta, content=message)
        return await super().send(msg)

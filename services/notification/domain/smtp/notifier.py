from pydantic import EmailStr
from datetime import datetime, UTC
from email.message import EmailMessage as _EmailMessage
from email.utils import format_datetime
from email.policy import Policy
from ..base.models import Log, BaseMessage, BaseMessageMeta
from ..base.protocols import IMessageSender
from ..base.notifier import BaseNotifier
from ...common.enums import NotificationChannel
from .utils import cut_to_length


# NOTESTED
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
SMTPGateway = IMessageSender[SMTPMessage]


# NOTESTED
class SMTPNotifier(BaseNotifier[SMTPMessage]):

    def _get_service_name(self) -> NotificationChannel:
        return NotificationChannel.EMAIL

    async def send(self, message: EmailMessage) -> Log[SMTPMessage]:
        meta = SMTPMessageMeta(
            sender=message["From"],
            recipient=message["To"],
            title=(
                cut_to_length(message["Subject"], 250)
                if message["Subject"]
                else "email message"
            ),
        )
        msg = SMTPMessage(meta=meta, content=message)
        return await super().send(msg)

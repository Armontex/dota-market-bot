from pydantic import EmailStr
from datetime import datetime, UTC
from email.message import EmailMessage as _EmailMessage
from email.utils import format_datetime
from email.policy import Policy

from sqlalchemy.ext.asyncio import AsyncSession
from .utils import cut_to_length
from ..base import Log, BaseMessage, BaseMessageMeta, IMessageSender, BaseNotifier
from ...common.enums import NotificationChannel


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
ISMTPSender = IMessageSender[SMTPMessage]


# NOTESTED
class SMTPNotifier(BaseNotifier[SMTPMessage]):

    def __init__(self, sender: ISMTPSender, session: AsyncSession) -> None:
        super().__init__(sender, session)

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

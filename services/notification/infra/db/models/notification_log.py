import sqlalchemy as sa
from common.db import Base
from common.decorators import abstract_model
from ....common.enums import MessageStatus, NotificationChannel
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


@abstract_model
class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel: Mapped[NotificationChannel] = mapped_column(
        sa.Enum(NotificationChannel, name="notification_channel"), nullable=False
    )
    title: Mapped[str] = mapped_column(sa.String(length=255), nullable=False)
    status: Mapped[MessageStatus] = mapped_column(
        sa.Enum(MessageStatus, name="message_status"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )

    __mapper_args__ = {"polymorphic_on": channel}


class EmailNotificationLog(NotificationLog):
    __tablename__ = "email_notification_logs"

    id: Mapped[int] = mapped_column(
        sa.ForeignKey("notification_logs.id"), primary_key=True
    )
    sender: Mapped[str] = mapped_column(sa.String(length=255), nullable=False)
    recipient: Mapped[str] = mapped_column(sa.String(length=255), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": NotificationChannel.EMAIL,
    }


class TelegramNotificationLog(NotificationLog):
    __tablename__ = "telegram_notification_logs"

    id: Mapped[int] = mapped_column(
        sa.ForeignKey("notification_logs.id"), primary_key=True
    )
    chat_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": NotificationChannel.TELEGRAM,
    }

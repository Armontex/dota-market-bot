import pytest
from http import HTTPStatus
from infra.notifiers.smtp import SMTPNotifier, EmailMessage


@pytest.mark.parametrize(
    "message",
    [EmailMessage("sender@smtp.com", "recipient@smtp.com", subject="Test")],
)
async def test_smtp_notifier(message, gateway):

    notifier = SMTPNotifier(gateway)
    result = await notifier.send(message)

    gateway.send_message.assert_awaited_once()
    assert (
        result.message.meta.sender == message["From"]
        and result.message.meta.recipient == message["To"]
        and result.message.meta.title == message["Subject"]
        and result.message.content == message
        and isinstance(result.status, HTTPStatus)
    )

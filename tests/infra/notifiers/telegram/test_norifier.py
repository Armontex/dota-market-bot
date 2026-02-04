import pytest
from http import HTTPStatus
from infra.notifiers.telegram import TelegramNotifier, TextContent, PhotoContent


@pytest.mark.parametrize(
    ["chat_id", "title", "content"],
    [
        [123123, "notify", TextContent(text="text")],
        [123123, "notify", PhotoContent(photo=bytes(1))],
        [12234, "notify", PhotoContent(photo=bytes(1), caption="caption")],
    ],
)
async def test_telegram_notifier(chat_id, title, content, gateway):

    notifier = TelegramNotifier(gateway)
    result = await notifier.send(chat_id, title, content)

    gateway.send_message.assert_awaited_once()
    assert (
        result.message.meta.sender == "bot"
        and result.message.meta.recipient == chat_id
        and result.message.meta.title == title
        and result.message.content == content
        and isinstance(result.status, HTTPStatus)
    )

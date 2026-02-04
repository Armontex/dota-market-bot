from http import HTTPStatus
from infra.notifiers.base import (
    BaseNotifier,
    BaseMessage,
    BaseMessageMeta,
    NotificationLog,
)


async def test_base_notifier(gateway):

    class ConcreteMeta(BaseMessageMeta[str, str]): ...

    class ConcreteMessage(BaseMessage[ConcreteMeta, str]): ...

    class ConcreteNotifier(BaseNotifier[ConcreteMessage]):
        def _get_service_name(self) -> str:
            return "ConcreteService"

    meta = ConcreteMeta(sender="0", recipient="1", title="title")
    msg = ConcreteMessage(meta=meta, content="content")
    Log = NotificationLog[ConcreteMessage]

    notifier = ConcreteNotifier(gateway)
    result = await notifier.send(msg)

    gateway.send_message.assert_awaited_once_with(msg)
    assert result == Log(message=msg, status=HTTPStatus.OK)

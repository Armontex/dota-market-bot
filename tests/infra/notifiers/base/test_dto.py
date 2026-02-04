import pytest
from infra.notifiers.base import BaseMessageMeta


def test_base_message_meta():
    class ConcreteMeta(BaseMessageMeta[str, str]): ...

    with pytest.raises(ValueError):
        ConcreteMeta(sender="", recipient="", title="123")
        ConcreteMeta(sender="", recipient="123", title="123")
        ConcreteMeta(sender="123", recipient="", title="123")

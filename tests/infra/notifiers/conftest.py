import pytest
from http import HTTPStatus
from unittest.mock import AsyncMock
from infra.notifiers.base import INotifyGateway


@pytest.fixture
def gateway() -> INotifyGateway:
    send_message = AsyncMock()
    send_message.return_value = HTTPStatus.OK
    gateway = AsyncMock()
    gateway.send_message = send_message
    return gateway

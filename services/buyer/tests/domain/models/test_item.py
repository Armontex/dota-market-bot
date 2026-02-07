import pytest
from services.buyer.domain.models import Item


@pytest.mark.parametrize(
    ["preferred_price", "max_price", "expected_error"],
    [
        [50, 100, None],
        [-100, 100, ValueError],
        [100, -100, ValueError],
        [100, 50, ValueError],
        [0, 100, ValueError],
        [100, 0, ValueError],
        [0, 0, ValueError],
        [-1, -1, ValueError],
    ],
)
def test_item(preferred_price, max_price, expected_error):
    if expected_error:
        with pytest.raises(expected_error):
            Item(preferred_price=preferred_price, max_price=max_price)
    else:
        Item(preferred_price=preferred_price, max_price=max_price)

import pytest
from services.seller.domain.models import Item


@pytest.mark.parametrize(
    ["preferred_price", "min_price", "min_step", "expected_error"],
    [
        [100, 50, 1, None],  # валидный случай
        [50, 50, 1, None],  # равные цены, валидно
        [50, 100, 1, ValueError],  # preferred_price < min_price
        [-100, 50, 1, ValueError],  # отрицательный preferred_price
        [100, -50, 1, ValueError],  # отрицательный min_price
        [100, 50, 0, ValueError],  # min_step <= 0
        [100, 50, -1, ValueError],  # отрицательный min_step
        [0, 50, 1, ValueError],  # preferred_price = 0
        [100, 0, 1, ValueError],  # min_price = 0
    ],
)
def test_item(preferred_price, min_price, min_step, expected_error):
    if expected_error:
        with pytest.raises(expected_error):
            Item(
                preferred_price=preferred_price, min_price=min_price, min_step=min_step
            )
    else:
        Item(preferred_price=preferred_price, min_price=min_price, min_step=min_step)

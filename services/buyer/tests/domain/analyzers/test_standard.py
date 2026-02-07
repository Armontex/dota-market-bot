import pytest
from unittest.mock import Mock
from services.buyer.domain.analyzers import StandardMarketAnalyzer
from services.buyer.domain.models import Decision


@pytest.mark.parametrize(
    ["expected", "best_price", "max_price", "preferred_price"],
    [
        [Decision(price=50), 50, 100, 70],
        [Decision(price=80), 80, 100, 70],
        [Decision(price=70), 120, 100, 70],
        [Decision(price=70), None, 100, 70],
    ],
)
def test_standard(expected, best_price, max_price, preferred_price):

    sell_offers = Mock()
    sell_offers.best_price = best_price

    market_info = Mock()
    market_info.sell_offers = sell_offers

    item = Mock()
    item.max_price = max_price
    item.preferred_price = preferred_price

    analyzer = StandardMarketAnalyzer(market_info)
    assert analyzer.calc_buying_price(item) == expected

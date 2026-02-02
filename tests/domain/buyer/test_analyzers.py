import pytest
from unittest.mock import Mock
from domain.buyer.analyzers import StandardShoppingMarketAnalyzer


@pytest.mark.parametrize(
    ["expected", "best_price", "max_price", "preferred_price"],
    [[50, 50, 100, 70], [80, 80, 100, 70], [70, 120, 100, 70], [70, None, 100, 70]],
)
def test_standard(expected, best_price, max_price, preferred_price):

    sell_offers = Mock()
    sell_offers.best_price = best_price

    market_info = Mock()
    market_info.sell_offers = sell_offers

    item = Mock()
    item.max_price = max_price
    item.preferred_price = preferred_price

    analyzer = StandardShoppingMarketAnalyzer(market_info)
    assert analyzer.calc_buying_price(item) == expected

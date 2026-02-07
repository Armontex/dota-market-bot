import pytest
from unittest.mock import Mock
from services.seller.domain.analyzers import StandardMarketAnalyzer
from services.seller.domain.models import Decision


@pytest.mark.parametrize(
    ["expected", "best_price", "min_price", "min_step"],
    [
        [Decision(price=49), 50, 40, 1],  # best_offer - min_step >= min_price
        [Decision(price=79), 80, 70, 1],  # best_offer - min_step >= min_price
        [
            Decision(price=50),
            51,
            50,
            2,
        ],  # best_offer - min_step < min_price → min_price возвращается
        [Decision(price=50), None, 50, 1],  # нет best_offer → min_price возвращается
        [
            Decision(price=50),
            51,
            50,
            1,
        ],  # best_offer - min_step = min_price → возвращается best_offer - min_step
    ],
)
def test_standard_sales(expected, best_price, min_price, min_step):
    sell_offers = Mock()
    sell_offers.best_price = best_price

    market_info = Mock()
    market_info.sell_offers = sell_offers

    item = Mock()
    item.min_price = min_price
    item.min_step = min_step

    analyzer = StandardMarketAnalyzer(market_info)
    assert analyzer.calc_selling_price(item) == expected

import pytest
from unittest.mock import Mock
from domain.seller.analyzers import StandardSalesMarketAnalyzer


@pytest.mark.parametrize(
    ["expected", "best_price", "min_price", "min_step"],
    [
        [49, 50, 40, 1],  # best_offer - min_step >= min_price
        [79, 80, 70, 1],  # best_offer - min_step >= min_price
        [50, 51, 50, 2],  # best_offer - min_step < min_price → min_price возвращается
        [50, None, 50, 1],  # нет best_offer → min_price возвращается
        [
            50,
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

    analyzer = StandardSalesMarketAnalyzer(market_info)
    assert analyzer.calc_selling_price(item) == expected

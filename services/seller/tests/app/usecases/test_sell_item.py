from unittest.mock import Mock
from services.seller.app.usecases import SellItemUseCase
from services.seller.domain.models import Decision


def test_sell_decision():
    expected = Decision(price=123)

    item = Mock()
    analyzer = Mock()
    analyzer.calc_selling_price.return_value = expected

    decision = SellItemUseCase(analyzer)
    assert decision.execute(item) == expected

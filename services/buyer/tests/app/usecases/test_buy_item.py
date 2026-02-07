from unittest.mock import Mock
from services.buyer.app.usecases import BuyItemUseCase
from services.buyer.domain.models import Decision


def test_buy_decision():
    expected = Decision(price=123)

    item = Mock()
    analyzer = Mock()
    analyzer.calc_buying_price.return_value = expected

    decision = BuyItemUseCase(analyzer)
    assert decision.execute(item) == expected

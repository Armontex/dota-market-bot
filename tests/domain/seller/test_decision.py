from unittest.mock import Mock
from domain.seller.sell_decision import SellDecision, SellDecisionAnswer


def test_sell_decision():
    expected = 123

    item = Mock()
    analyzer = Mock()
    analyzer.calc_selling_price.return_value = expected

    decision = SellDecision(item, analyzer=analyzer)
    assert decision.decide() == SellDecisionAnswer(price=expected)

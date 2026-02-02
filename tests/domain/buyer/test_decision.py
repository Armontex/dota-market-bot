from unittest.mock import Mock
from domain.buyer.buy_decision import BuyDecision, BuyDecisionAnswer


def test_buy_decision():
    expected = 123

    item = Mock()
    analyzer = Mock()
    analyzer.calc_buying_price.return_value = expected

    decision = BuyDecision(item, analyzer=analyzer)
    assert decision.decide() == BuyDecisionAnswer(price=expected)

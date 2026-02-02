from domain.common.base import Decision
from .base import ShoppingMarketAnalyzer
from .dto.incoming import BuyItem
from .dto.outgoing import BuyDecisionAnswer


class BuyDecision(Decision):

    def __init__(
        self,
        item: BuyItem,
        *,
        analyzer: ShoppingMarketAnalyzer,
    ) -> None:
        self._item = item
        self._analyzer = analyzer

    def decide(self) -> BuyDecisionAnswer:
        return BuyDecisionAnswer(price=self._analyzer.calc_buying_price(self._item))

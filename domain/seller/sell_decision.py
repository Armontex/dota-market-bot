from domain.common.base import Decision
from .base import SalesMarketAnalyzer
from .dto.incoming import SellItem
from .dto.outgoing import SellDecisionAnswer


class SellDecision(Decision):

    def __init__(
        self,
        item: SellItem,
        *,
        analyzer: SalesMarketAnalyzer,
    ) -> None:
        self._item = item
        self._analyzer = analyzer

    def decide(self) -> SellDecisionAnswer:
        return SellDecisionAnswer(price=self._analyzer.calc_selling_price(self._item))

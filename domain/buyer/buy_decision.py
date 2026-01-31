from domain.common.base import Decision
from .base import ShoppingMarketAnalyzer
from .value_objects import BuyItemVO
from .ports.dto import BuyDecisionDTO


class BuyDecision(Decision):

    def __init__(
        self,
        item: BuyItemVO,
        *,
        analyzer: ShoppingMarketAnalyzer,
    ) -> None:
        self._item = item
        self._analyzer = analyzer

    def decide(self) -> BuyDecisionDTO:
        return BuyDecisionDTO(price=self._analyzer.calc_buying_price(self._item))

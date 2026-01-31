from .base import Decision, SalesMarketAnalyzer
from .value_objects import SellItemVO
from .ports.dto.sell import SellDecisionDTO


class SellDecision(Decision):

    def __init__(
        self,
        item: SellItemVO,
        *,
        analyzer: SalesMarketAnalyzer,
    ) -> None:
        self._item = item
        self._analyzer = analyzer

    def decide(self) -> SellDecisionDTO:
        return SellDecisionDTO(
            price=self._analyzer.calc_selling_price(self._item),
            time_of_next_check=self._analyzer.calc_time_of_next_check(),
        )

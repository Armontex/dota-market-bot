from ...domain.models import Decision, Item, MarketInfo
from ...domain.analyzers import BaseMarketAnalyzer


class SellItemUseCase:

    def __init__(self, analyzer: BaseMarketAnalyzer) -> None:
        self._analyzer = analyzer

    def execute(self, item: Item, /, market_info: MarketInfo) -> Decision:
        return self._analyzer.calc_selling_price(item)

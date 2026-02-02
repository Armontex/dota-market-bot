from .dto.incoming import SellItem, MarketInfo
from .base import SalesMarketAnalyzer


class StandardSalesMarketAnalyzer(SalesMarketAnalyzer):

    def calc_selling_price(self, item: SellItem) -> int:
        best_offer = self._info.sell_offers.best_price
        if best_offer and (best_offer - item.min_step) >= item.min_price:
            return best_offer - item.min_step
        return item.min_price


class SalesAnalyzersFactory:

    @staticmethod
    def get_standart_sales_analyzer(
        market_info: MarketInfo,
    ) -> StandardSalesMarketAnalyzer:
        return StandardSalesMarketAnalyzer(market_info)

from datetime import datetime, timedelta, UTC
from .value_objects import SellItemVO
from .ports.dto.sell import MarketInfo
from .base import SalesMarketAnalyzer


class StandardSalesMarketAnalyzer(SalesMarketAnalyzer):

    def calc_selling_price(self, item: SellItemVO) -> float:
        best_offer = self._info.sell_offers.best_offer
        if best_offer and (best_offer - item.min_step) >= item.min_price:
            return best_offer - item.min_step
        return item.min_price

    def calc_time_of_next_check(self) -> datetime:
        return datetime.now(UTC) + timedelta(minutes=5)


class AnalyzersFactory:

    @staticmethod
    def get_standart_sales_analyzer(market_info: MarketInfo) -> SalesMarketAnalyzer:
        return StandardSalesMarketAnalyzer(market_info)

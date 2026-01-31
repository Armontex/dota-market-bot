from .value_objects import BuyItemVO
from .ports.dto import MarketInfo
from .base import ShoppingMarketAnalyzer


class StandartShoppingMarketAnalyzer(ShoppingMarketAnalyzer):

    def calc_buying_price(self, item: BuyItemVO) -> float:
        best_offer = self._info.sell_offers.best_offer
        if best_offer and (best_offer <= item.max_price):
            return best_offer
        return item.preferred_price


class ShoppingAnalyzersFactory:

    @staticmethod
    def get_standart_sales_analyzer(
        market_info: MarketInfo,
    ) -> StandartShoppingMarketAnalyzer:
        return StandartShoppingMarketAnalyzer(market_info)

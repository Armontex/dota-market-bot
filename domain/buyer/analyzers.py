from .dto.incoming import BuyItem, MarketInfo
from .base import ShoppingMarketAnalyzer


class StandartShoppingMarketAnalyzer(ShoppingMarketAnalyzer):

    def calc_buying_price(self, item: BuyItem) -> int:
        best_offer = self._info.sell_offers.best_price
        if best_offer and (best_offer <= item.max_price):
            return best_offer
        return item.preferred_price


class ShoppingAnalyzersFactory:

    @staticmethod
    def get_standart_sales_analyzer(
        market_info: MarketInfo,
    ) -> StandartShoppingMarketAnalyzer:
        return StandartShoppingMarketAnalyzer(market_info)

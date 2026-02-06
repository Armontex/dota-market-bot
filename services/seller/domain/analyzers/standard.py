from .base import BaseMarketAnalyzer
from ..models import Item, Decision


class StandardMarketAnalyzer(BaseMarketAnalyzer):

    def calc_selling_price(self, item: Item) -> Decision:
        best_offer = self._info.sell_offers.best_price
        price = item.min_price
        if best_offer and (best_offer - item.min_step) >= item.min_price:
            price = best_offer - item.min_step

        return Decision(price=price)

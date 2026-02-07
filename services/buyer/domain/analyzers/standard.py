from ..models import Item, Decision
from .base import BaseMarketAnalyzer


class StandardMarketAnalyzer(BaseMarketAnalyzer):
    """
    Анализирует рынок и принимает решение о покупке предмета.
    """

    def calc_buying_price(self, item: Item) -> Decision:
        """Вычисляет цену покупки для указанного предмета.

        Args:
            item: Объект предмета, для которого нужно рассчитать цену покупки.

        Returns:
            Decision: Объект решения, содержащий рекомендуемую цену покупки.
        """
        best_offer = self._info.sell_offers.best_price
        price = item.preferred_price
        if best_offer and (best_offer <= item.max_price):
            price = best_offer
        return Decision(price=price)

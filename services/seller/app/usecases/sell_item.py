from ...domain.models import Decision, Item
from ...domain.analyzers import BaseMarketAnalyzer


class SellItemUseCase:
    "Класс `SellItemUseCase` берет предмет и использует анализатор рынка для расчета цены продажи."

    def __init__(self, analyzer: BaseMarketAnalyzer) -> None:
        self._analyzer = analyzer

    def execute(self, item: Item) -> Decision:
        """
        Вычисляет решение о продаже предмета, используя анализатор рынка.

        Args:
            item (Item): Объект предмета, для которого нужно принять решение о продаже.

        Returns:
            Decision: Решение о продаже, содержащее информацию о цене и других параметрах.
        """
        return self._analyzer.calc_selling_price(item)

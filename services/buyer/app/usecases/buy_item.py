from ...domain.models import Decision, Item
from ...domain.analyzers import BaseMarketAnalyzer


class BuyItemUseCase:
    """
    UseCase для принятия решения о покупке предмета.

    Этот класс использует переданный анализатор рынка для вычисления цены,
    по которой можно купить предмет, исходя из его параметров.
    """

    def __init__(self, analyzer: BaseMarketAnalyzer) -> None:
        self._analyzer = analyzer

    def execute(self, item: Item) -> Decision:
        """
        Выполняет логику вычисления цены покупки для указанного предмета.

        Args:
            item (Item): Объект предмета, содержащий информацию о предпочтительной
                и максимальной цене
        Returns:
            Decision: Решение о цене покупки
        """
        return self._analyzer.calc_buying_price(item)

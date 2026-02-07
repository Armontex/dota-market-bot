from abc import ABC, abstractmethod
from ..models import MarketInfo, Item, Decision


class BaseMarketAnalyzer(ABC):
    """Базовый класс для аналитических моделей рынка.

    Предоставляет интерфейс для расчета цен продажи предметов на рынке Dota.
    """

    def __init__(self, market_info: MarketInfo) -> None:
        """Инициализирует анализатор информацией о рынке.

        Args:
            market_info: Объект с информацией о рынке.
        """
        self._info = market_info

    @abstractmethod
    def calc_selling_price(self, item: Item) -> Decision:
        """Вычисляет решение о цене продажи предмета.

        Args:
            item: Объект предмета, для которого рассчитывается цена продажи.

        Returns:
            Решение о цене продажи.
        """
        raise NotImplementedError()

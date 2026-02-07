from abc import ABC, abstractmethod
from ..models import MarketInfo, Item, Decision


class BaseMarketAnalyzer(ABC):
    """Абстрактный базовый класс для анализа рынка и принятия решений о покупке предметов.

    Этот класс определяет общий интерфейс для всех анализаторов рынка,
    которые должны реализовать метод расчета цены покупки.
    """

    def __init__(self, market_info: MarketInfo) -> None:
        """Инициализирует анализатор информацией о рынке.

        Args:
            market_info: Объект с информацией о рынке, который будет использоваться
                        для анализа и принятия решений.
        """
        self._info = market_info

    @abstractmethod
    def calc_buying_price(self, item: Item) -> Decision:
        """Вычисляет рекомендуемую цену покупки для указанного предмета.

        Args:
            item: Объект предмета, для которого нужно рассчитать цену покупки.

        Returns:
            Решение о покупке, содержащее рекомендуемую цену и другие параметры.
        """
        raise NotImplementedError()

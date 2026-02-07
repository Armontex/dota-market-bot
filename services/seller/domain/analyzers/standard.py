from .base import BaseMarketAnalyzer
from ..models import Item, Decision


class StandardMarketAnalyzer(BaseMarketAnalyzer):
    """
    Стандартный анализатор рыночных предложений для определения цены продажи предмета.

    Использует стратегию "перебития" лучшей текущей цены продажи с учетом минимального шага,
    при этом не опускаясь ниже минимальной разрешенной цены предмета.
    """

    def calc_selling_price(self, item: Item) -> Decision:
        """
        Рассчитывает оптимальную цену продажи для указанного предмета.

        Алгоритм:
        1. Получает лучшую текущую цену предложения на продажу
        2. Если такая цена существует и позволяет сделать "перебитие" с учетом минимального шага,
           устанавливает цену продажи как (лучшая_цена_предложения - минимальный_шаг)
        3. В противном случае использует минимальную разрешенную цену предмета

        Args:
            item: Объект Item, содержащий информацию о предмете, включая
                  минимальную цену (min_price) и минимальный шаг (min_step)

        Returns:
            Decision: Объект решения с рассчитанной ценой продажи
        """
        best_offer = self._info.sell_offers.best_price
        price = item.min_price
        if best_offer and (best_offer - item.min_step) >= item.min_price:
            price = best_offer - item.min_step

        return Decision(price=price)

from abc import ABC, abstractmethod
from ..models import MarketInfo, Item, Decision


class BaseMarketAnalyzer(ABC):

    def __init__(self, market_info: MarketInfo) -> None:
        self._info = market_info

    @abstractmethod
    def calc_selling_price(self, item: Item) -> Decision:
        raise NotImplementedError()

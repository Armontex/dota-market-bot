from abc import ABC, abstractmethod
from .dto.incoming import MarketInfo, BuyItem


class ShoppingMarketAnalyzer(ABC):

    def __init__(self, market_info: MarketInfo) -> None:
        self._info = market_info

    @abstractmethod
    def calc_buying_price(self, item: BuyItem) -> int:
        raise NotImplementedError()

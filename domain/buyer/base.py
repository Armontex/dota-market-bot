from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from .dto.incoming import MarketInfo, BuyItem


class ShoppingMarketAnalyzer(ABC):

    def __init__(self, market_info: MarketInfo) -> None:
        self._info = market_info

    @abstractmethod
    def calc_buying_price(self, item: BuyItem) -> int:
        raise NotImplementedError()

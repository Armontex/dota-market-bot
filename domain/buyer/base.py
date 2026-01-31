from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from .ports.dto import MarketInfo
    from .value_objects import BuyItemVO


class ShoppingMarketAnalyzer(ABC):

    def __init__(self, market_info: MarketInfo) -> None:
        self._info = market_info

    @abstractmethod
    def calc_buying_price(self, item: BuyItemVO) -> float:
        raise NotImplementedError()

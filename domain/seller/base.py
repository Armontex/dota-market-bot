from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from .dto.incoming import MarketInfo, SellItem


class SalesMarketAnalyzer(ABC):

    def __init__(self, market_info: MarketInfo) -> None:
        self._info = market_info

    @abstractmethod
    def calc_selling_price(self, item: SellItem) -> int:
        raise NotImplementedError()

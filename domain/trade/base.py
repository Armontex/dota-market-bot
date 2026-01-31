from typing import TYPE_CHECKING
from datetime import datetime
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from .ports.dto.sell import MarketInfo
    from .value_objects import SellItemVO


class Decision(ABC):

    @abstractmethod
    def decide(self):
        raise NotImplementedError()


class SalesMarketAnalyzer(ABC):

    def __init__(self, market_info: MarketInfo) -> None:
        self._info = market_info

    @abstractmethod
    def calc_selling_price(self, item: SellItemVO) -> float:
        raise NotImplementedError()

    @abstractmethod
    def calc_time_of_next_check(self) -> datetime:
        raise NotImplementedError()

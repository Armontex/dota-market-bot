from pydantic import BaseModel
from domain.common.ports.dto import Offers, History


class MarketInfo(BaseModel):
    sell_offers: Offers  # Офферы на продажу
    buy_offers: Offers  # Офферы на покупку
    history: History  # История продаж


class SellDecisionDTO(BaseModel):
    price: float  # Цена продажи (в руб.)
from pydantic import BaseModel
from domain.common.ports.dto import Offers, History


class MarketInfo(BaseModel):
    sell_offers: Offers  # Офферы на продажу
    history: History  # История продаж


class BuyDecisionDTO(BaseModel):
    price: float

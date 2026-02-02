from pydantic import Field
from domain.common.base import DTO


class BuyDecisionAnswer(DTO):
    price: int = Field(..., description="Цена покупки (в копейках)")

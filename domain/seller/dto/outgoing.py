from pydantic import Field
from domain.common.base import DTO


class SellDecisionAnswer(DTO):
    price: int = Field(..., description="Цена продажи (в копейках)")

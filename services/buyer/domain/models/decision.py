from pydantic import Field
from common.dto import DTO


class Decision(DTO):
    price: int = Field(..., description="Цена покупки (в копейках)")

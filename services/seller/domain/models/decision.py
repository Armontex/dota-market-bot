from pydantic import Field
from common.pydantic_models import DTO


class Decision(DTO):
    price: int = Field(..., description="Цена продажи (в копейках)")

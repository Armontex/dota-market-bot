from typing import Self
from pydantic import Field, field_validator, model_validator
from domain.common.base import DTO
from domain.common.dto.incoming import Offers, History


class MarketInfo(DTO):
    sell_offers: Offers = Field(..., description="Офферы на продажу")
    history: History = Field(..., description="История продаж")


class BuyItem(DTO):
    preferred_price: int = Field(..., description="Предпочтительная цена (в копейках)")
    max_price: int = Field(..., description="Максимальная цена (в копейках)")

    @field_validator("preferred_price")
    @classmethod
    def validate_preferred_price(cls, v: int):
        if v <= 0:
            raise ValueError(f"preferred_price должен быть > 0, получено {v}")
        return v

    @field_validator("max_price")
    @classmethod
    def validate_max_price(cls, v: int):
        if v <= 0:
            raise ValueError(f"max_price должен быть > 0, получено {v}")
        return v

    @model_validator(mode="after")
    def validate_prices(self) -> Self:
        if self.max_price < self.preferred_price:
            raise ValueError(
                f"max_price ({self.max_price}) не может быть меньше preferred_price ({self.preferred_price})"
            )
        return self

from pydantic import Field, field_validator, model_validator
from common.dto import DTO
from typing import Self


class Item(DTO):
    preferred_price: int = Field(..., description="Предпочтительная цена (в копейках)")
    min_price: int = Field(..., description="Минимальная цена (в копейках)")
    min_step: int = Field(1, description="Минимальный шаг перебития цены (в копейках)")

    @field_validator("preferred_price")
    @classmethod
    def validate_preferred_price(cls, v: int):
        if v <= 0:
            raise ValueError(f"preferred_price должен быть > 0, получено {v}")
        return v

    @field_validator("min_price")
    @classmethod
    def validate_min_price(cls, v: int):
        if v <= 0:
            raise ValueError(f"min_price должен быть > 0, получено {v}")
        return v

    @field_validator("min_step")
    @classmethod
    def validate_min_step(cls, v: int):
        if v <= 0:
            raise ValueError(f"min_step должен быть > 0, получено {v}")

    @model_validator(mode="after")
    def validate_prices(self) -> Self:
        if self.preferred_price < self.min_price:
            raise ValueError(
                f"preferred_price ({self.preferred_price}) не может быть меньше min_price ({self.min_price})"
            )
        return self

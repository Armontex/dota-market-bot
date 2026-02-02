import pytest
from domain.seller.dto.incoming import SellItem


# class SellItem(BaseModel):
#     preferred_price: int = Field(..., description="Предпочтительная цена (в копейках)")
#     min_price: int = Field(..., description="Минимальная цена (в копейках)")
#     min_step: int = Field(1, description="Минимальный шаг перебития цены (в копейках)")

#     @field_validator("preferred_price")
#     @classmethod
#     def validate_preferred_price(cls, v: int):
#         if v <= 0:
#             raise ValueError(f"preferred_price должен быть > 0, получено {v}")
#         return v

#     @field_validator("min_price")
#     @classmethod
#     def validate_min_price(cls, v: int):
#         if v <= 0:
#             raise ValueError(f"min_price должен быть > 0, получено {v}")
#         return v

#     @field_validator("min_step")
#     @classmethod
#     def validate_min_step(cls, v: int):
#         if v <= 0:
#             raise ValueError(f"min_step должен быть > 0, получено {v}")

#     @model_validator(mode="after")
#     def validate_prices(self) -> Self:
#         if self.preferred_price < self.min_price:
#             raise ValueError(
#                 f"preferred_price ({self.preferred_price}) не может быть меньше min_price ({self.min_price})"
#             )
#         return self


@pytest.mark.parametrize(
    ["preferred_price", "min_price", "min_step", "expected_error"],
    [
        [100, 50, 1, None],  # валидный случай
        [50, 50, 1, None],  # равные цены, валидно
        [50, 100, 1, ValueError],  # preferred_price < min_price
        [-100, 50, 1, ValueError],  # отрицательный preferred_price
        [100, -50, 1, ValueError],  # отрицательный min_price
        [100, 50, 0, ValueError],  # min_step <= 0
        [100, 50, -1, ValueError],  # отрицательный min_step
        [0, 50, 1, ValueError],  # preferred_price = 0
        [100, 0, 1, ValueError],  # min_price = 0
    ],
)
def test_sellitem(preferred_price, min_price, min_step, expected_error):
    if expected_error:
        with pytest.raises(expected_error):
            SellItem(
                preferred_price=preferred_price, min_price=min_price, min_step=min_step
            )
    else:
        SellItem(
            preferred_price=preferred_price, min_price=min_price, min_step=min_step
        )

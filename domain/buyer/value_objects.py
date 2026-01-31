from dataclasses import dataclass


@dataclass(frozen=True)
class BuyItemVO:
    preferred_price: float  # Предпочтительная цена (в руб.)
    max_price: float  # Минимальная цена (в руб.)

    def __post_init__(self):
        if self.max_price < 0:
            raise ValueError(f"max_price должен быть >= 0, получено {self.max_price}")
        if self.preferred_price < self.max_price:
            raise ValueError(
                f"preferred_price ({self.preferred_price}) не может быть меньше max_price ({self.max_price})"
            )
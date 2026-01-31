from dataclasses import dataclass


@dataclass(frozen=True)
class SellItemVO:
    preferred_price: float  # Предпочтительная цена (в руб.)
    min_price: float  # Минимальная цена (в руб.)
    min_step: float = 0.01  # Минимальный шаг перебития цены (в руб.)

    def __post_init__(self):
        if self.min_price < 0:
            raise ValueError(f"min_price должен быть >= 0, получено {self.min_price}")
        if self.preferred_price < self.min_price:
            raise ValueError(
                f"preferred_price ({self.preferred_price}) не может быть меньше min_price ({self.min_price})"
            )
        if self.min_step <= 0:
            raise ValueError(f"min_step должен быть > 0, получено {self.min_step}")

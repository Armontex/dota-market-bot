from pydantic import Field
from datetime import datetime
from common.dto import DTO


class Offer(DTO):
    price: int = Field(..., description="Цена оффера (в копейках)")
    count: int = Field(..., description="Кол-во таких офферов")


class Offers(DTO):
    best_price: int | None = Field(..., description="Цена лучшего оффера (в копейках)")
    offers: list[Offer] = Field(..., description="Офферы")


class Sale(DTO):
    price: int = Field(..., description="Цена продажи (в копейках)")
    timestamp: datetime = Field(..., description="Время продажи")


class History(DTO):
    max_price: int | None = Field(..., description="Максимальная цена (в копейках)")
    min_price: int | None = Field(..., description="Минимальная цена (в копейках)")
    average: int | None = Field(..., description="Средняя цена (в копейках)")
    count_sales: int = Field(..., description="Количество продаж")
    sales: list[Sale] = Field(..., description="Продажи")


class MarketInfo(DTO):
    sell_offers: Offers = Field(..., description="Офферы на продажу")
    buy_offers: Offers = Field(..., description="Офферы на покупку")
    history: History = Field(..., description="История покупок")

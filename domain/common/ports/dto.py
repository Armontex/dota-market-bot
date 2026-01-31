from pydantic import BaseModel
from datetime import datetime


class Sale(BaseModel):
    price: float  # Цена продажи (в руб.)
    time: datetime  # Дата продажи


class History(BaseModel):
    max_price: float | None  # Максимальная цена (в руб.)
    min_price: float | None  # Минимальная цена (в руб.)
    average: float | None  # Средняя цена (в руб.)
    number: int  # Кол-во продаж в истории
    sales: list[Sale]  # Продажи


class Offer(BaseModel):
    price: float  # Цена (в руб.)
    count: int  # Кол-во


class Offers(BaseModel):
    best_offer: float | None  # Цена лучшего оффера (в руб.)
    offers: list[Offer]  # Список офферов
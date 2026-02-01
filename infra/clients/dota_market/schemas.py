from pydantic import BaseModel, ConfigDict, Field


class Schema(BaseModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True)


class Sale(Schema):
    price: int = Field(alias="l_price")  # Копейки (руб.)
    timestamp: int = Field(alias="l_time")


class ItemHistorySchema(Schema):
    success: bool
    max_price: int = Field(alias="max")  # Копейки (руб.)
    min_price: int = Field(alias="min")  # Копейки (руб.)
    avg_price: int = Field(alias="average")  # Копейки (руб.)
    count_sales: int = Field(alias="number")
    history: list[Sale]


class SellOffer(Schema):
    price: int  # Копейки (руб.)
    count_offers: int = Field(alias="count")
    my_count_offers: int = Field(alias="my_count")


class SellOffersSchema(Schema):
    success: bool
    best_offer_price: int = Field(alias="best_offer")  # Копейки (руб.)
    offers: list[SellOffer]


class BuyOffer(Schema):
    price: int = Field(alias="o_price")  # Копейки (руб.)
    count_offers: int = Field(alias="c")
    my_count_offers: int = Field(alias="my_count")


class BuyOffersSchema(Schema):
    success: bool
    best_offer_price: int = Field(alias="best_offer")  # Копейки (руб.)
    offers: list[BuyOffer]

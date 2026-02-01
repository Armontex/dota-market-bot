from pydantic import BaseModel, ConfigDict


class Schema(BaseModel):
    model_config = ConfigDict(frozen=True)


class Sale(Schema):
    l_price: int  # Копейки (руб.)
    l_time: int


class ItemHistorySchema(Schema):
    success: bool
    max: int  # Копейки (руб.)
    min: int  # Копейки (руб.)
    average: int  # Копейки (руб.)
    number: int
    history: list[Sale]


class SellOffer(BaseModel):
    price: int  # Копейки (руб.)
    count: int
    my_count: int


class SellOffersSchema(BaseModel):
    success: bool
    best_offer: int  # Копейки (руб.)
    offers: list[SellOffer]


class BuyOffer(BaseModel):
    o_price: int  # Копейки (руб.)
    c: int  # count
    my_count: int


class BuyOffersSchema(BaseModel):
    success: bool
    best_offer: int  # Копейки (руб.)
    offers: list[BuyOffer]

from datetime import datetime
from typing import Any
from typing_extensions import Self

from pydantic import BaseModel, field_validator, model_validator


class ProductPayload(BaseModel):
    name: str
    price: float
    is_18_plus: bool = False

    @field_validator("price")
    def validate_price(cls, v):
        if v < 0:
            raise ValueError("Price can't be negative")
        return v

    @field_validator("name")
    def validate_name(cls, v):
        return v.capitalize()

    @model_validator(mode="before")
    def validate_price_and_is_18_plus(
        cls,
        data: Any,
    ) -> Self:
        if data["is_18_plus"] and data["price"] < 100:
            raise ValueError("Price must be 100 or higher for 18+ products")

        return data


class Product(ProductPayload):
    id: int
    created_at: datetime | None = None

    @classmethod
    def from_row(cls, row: tuple):
        return cls(
            id=row[0],
            name=row[1],
            price=row[2],
            is_18_plus=bool(row[3]),
            created_at=row[4]
        )

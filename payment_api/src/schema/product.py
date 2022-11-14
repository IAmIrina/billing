"""Pydantic models."""

from typing import Literal

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default) -> str:
    """Fast json dumps."""
    return orjson.dumps(v, default=default).decode()


class OrjsonModel(BaseModel):
    """Fast json serializer."""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ProductData(OrjsonModel):
    """Product info."""
    name: str
    description: str


class Product(OrjsonModel):
    """Payment product info."""
    unit_amount: int
    currency: Literal['usd']
    product_data: ProductData

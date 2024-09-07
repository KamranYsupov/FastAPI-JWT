from typing import TYPE_CHECKING

import strawberry

#from app.db import Product
from app.schemas.product import ProductSchema
from .seller import SellerType


@strawberry.type(name='Product')
class ProductType:
    id: str
    name: str
    description: str
    price: float
    rating: float
    seller: SellerType 

    @classmethod
    def from_data(cls, data: dict):
        return cls(**data)
       


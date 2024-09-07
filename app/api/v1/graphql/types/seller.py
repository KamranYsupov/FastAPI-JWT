from typing import TYPE_CHECKING, List

import strawberry

from app.db import Seller
from app.schemas.seller import SellerSchema


@strawberry.type(name='Seller')
class SellerType:
    id: str
    name: str
    bio: str
    is_verified: bool

   # db_obj: strawberry.Private[Seller]

   # @strawberry.field
   # def products(self) -> List[ProductType]:
  #      products = [
   #         ProductType.from_db_obj(product) 
   #         for product in self.db_obj.products
   #     ]
    #     
    #    return products
                                                                                        
    @classmethod
    def from_db_obj(cls, db_obj: Seller):
        return cls(
            id=db_obj.id,
            name=db_obj.name, 
            bio=db_obj.bio, 
            is_verified=db_obj.is_verified,
            db_obj=db_obj,
        )
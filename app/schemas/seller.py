import uuid
from typing import TYPE_CHECKING

from .mixins import SellerSchemaMixin

if not TYPE_CHECKING:
    from .product import ProductSchema


class SellerSchema(SellerSchemaMixin):
    id: uuid.UUID
                   

class SellerProductsSchema(SellerSchemaMixin):
    products: list['ProductSchema'] 
    
                       
class CreateSellerSchema(SellerSchemaMixin):
    user_id: uuid.UUID | None 
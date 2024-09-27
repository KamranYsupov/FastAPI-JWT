import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field

from .mixins import ProductSchemaMixin 

if TYPE_CHECKING:
    from .seller import SellerSchema


class ProductSchema(ProductSchemaMixin):
    seller: Optional['SellerSchema'] = Field(title='Продавец', default=None)
    id: uuid.UUID
    
    
class CreateProductSchema(ProductSchemaMixin):
    seller_id: Optional[uuid.UUID] = Field(title='ID продавца', default=None)
  
    

    
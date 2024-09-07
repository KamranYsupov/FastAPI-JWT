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
    
  
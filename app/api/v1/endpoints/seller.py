from typing import Dict, Any

from dependency_injector import providers
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, HTTPException
from starlette import status

from app.core.container import Container
from app.db import User
from app.schemas.seller import CreateSellerSchema, SellerSchema
from app.services.seller import SellerService
from app.utils.orm import validate_object_insertion
from ..deps import get_current_user_access

router = APIRouter(tags=['Seller'], prefix='/seller')

@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=SellerSchema,
)
@inject
async def create_seller(
    create_seller_schema: CreateSellerSchema,
    user: User = Depends(get_current_user_access),
    seller_service: SellerService = Depends(Provide[Container.seller_service]),
) -> SellerSchema:
    create_seller_schema.user_id = user.id
    seller = await validate_object_insertion(
        seller_service.create,
        insert_schema=create_seller_schema,
    )
    seller_schema = SellerSchema(
        id=seller.id,
        name=seller.name,
        bio=seller.bio,
        is_verified=seller.is_verified,
    )
    return seller_schema

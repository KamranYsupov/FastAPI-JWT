from fastapi import APIRouter

from app.core.config import settings
from .endpoints.user import router as user_router
from .endpoints.auth import router as auth_router
from .endpoints.seller import router as seller_router
from .endpoints.product import router as product_router
from .graphql import router as graphql_router


api_router = APIRouter()

# REST
api_router.include_router(user_router)
api_router.include_router(auth_router)
api_router.include_router(seller_router)
api_router.include_router(product_router)

# GraphQL
api_router.include_router(
    graphql_router,
    prefix=settings.graphql_prefix
)

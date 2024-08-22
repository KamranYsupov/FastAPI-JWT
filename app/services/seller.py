from uuid import UUID

from app.repositories.seller import RepositorySeller
from app.schemas.seller import CreateSellerSchema
from app.db import Seller


class SellerService:
    def __init__(
        self, 
        repository_seller: RepositorySeller,
        unique_fields: list[str] | tuple[str] | None = None,
    ):
        self._repository_seller = repository_seller
        self.unique_fields = unique_fields

    async def get(self, **kwargs) -> Seller:
        return await self._repository_seller.get(**kwargs)

    async def create(self, seller_schema: CreateSellerSchema) -> Seller:
        return await self._repository_seller.create(
            seller_schema,
            unique_fields=self.unique_fields
        )

    async def update(self, *, seller_id: UUID, obj_in) -> Seller:
        return await self._repository_seller.update(
            obj_id=seller_id,
            obj_in=obj_in,
            unique_fields=self.unique_fields
        )

    async def list(self, *args, **kwargs) -> list[Seller]:
        return await self._repository_seller.list(*args, **kwargs)

    async def delete(self, obj_id: UUID) -> None:
        return await self._repository_seller.delete(obj_id=obj_id)

    async def exists(self, *args, **kwargs) -> Seller | None:
        return await self._repository_seller.exists(*args, **kwargs)
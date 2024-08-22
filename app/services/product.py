from uuid import UUID

from app.repositories import RepositoryProduct
from app.db import Product
from app.schemas.product import CreateProductSchema


class ProductService:
    def __init__(
        self, 
        repository_product: RepositoryProduct,
        unique_fields: list[str] | tuple[str] | None = None,
    ):
        self._repository_product = repository_product
        self.unique_fields = unique_fields

    async def get(self, **kwargs) -> Product:
        return await self._repository_product.get(**kwargs)

    async def create(self, product_schema: CreateProductSchema) -> Product:
        return await self._repository_product.create(
            product_schema,
            unique_fields=self.unique_fields
        )

    async def update(self, *, product_id: UUID, obj_in) -> Product:
        return await self._repository_product.update(
            obj_id=product_id,
            obj_in=obj_in,
            unique_fields=self.unique_fields
        )

    async def list(self, *args, **kwargs) -> list[Product]:
        return await self._repository_product.list(*args, **kwargs)

    async def delete(self, obj_id: UUID) -> None:
        return await self._repository_product.delete(obj_id=obj_id)

    async def exists(self, *args, **kwargs) -> Product | None:
        return await self._repository_product.exists(*args, **kwargs)
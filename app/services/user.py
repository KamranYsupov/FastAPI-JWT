from uuid import UUID

from app.repositories.user import RepositoryUser
from app.schemas.user import CreateUserSchema
from app.db import User


class UserService:
    def __init__(
        self,
        repository_user: RepositoryUser,
        unique_fields: list[str] | tuple[str] | None = None,
    ):
        self._repository_user = repository_user
        self.unique_fields = unique_fields

    async def get(
        self, 
        join_seller: bool = False,
        **kwargs,
     ) -> User:
        return await self._repository_user.get(
            join_seller=join_seller, 
            **kwargs
        )

    async def create_user(self, user_schema: CreateUserSchema) -> User:
        return await self._repository_user.create_user(
            obj_in=user_schema.model_dump(),
            unique_fields=self.unique_fields
        )

    async def update(self, *, user_id: UUID, obj_in) -> User:
        return await self._repository_user.update(
            obj_id=user_id,
            obj_in=obj_in,
            unique_fields=self.unique_fields,
        )

    async def list(self, *args, **kwargs) -> list[User]:
        return await self._repository_user.list(*args, **kwargs)

    async def delete(self, obj_id: UUID) -> None:
        return await self._repository_user.delete(obj_id=obj_id)

    async def exists(self, *args, **kwargs) -> User | None:
        return await self._repository_user.exists(*args, **kwargs)

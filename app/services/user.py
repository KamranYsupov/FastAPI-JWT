from uuid import UUID

from app.repositories.user import RepositoryUser
from app.schemas.user import CreateUserSchema


class UserService:
    def __init__(self, repository_user: RepositoryUser):
        self._repository_user = repository_user

    async def get(self, **kwargs):
        return await self._repository_user.get(**kwargs)

    async def create_user(self, user_schema: CreateUserSchema):
        return await self._repository_user.create_user(user_schema.model_dump())

    async def update(self, *, user_id: UUID, obj_in):
        return await self._repository_user.update(
            obj_id=user_id,
            obj_in=obj_in
        )

    async def list(self, *args, **kwargs):
        return await self._repository_user.list(*args, **kwargs)

    async def delete(self, obj_id: UUID) -> None:
        return await self._repository_user.delete(obj_id=obj_id)

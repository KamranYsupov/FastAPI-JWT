from uuid import UUID

from fastapi import HTTPException
from starlette import status

from app.repositories.user import RepositoryUser
from app.schemas.user import CreateUserSchema
from app.db import User


class UserService:
    def __init__(self, repository_user: RepositoryUser):
        self._repository_user = repository_user

    async def get(self, **kwargs) -> User:
        return await self._repository_user.get(**kwargs)

    async def create_user(self, user_schema: CreateUserSchema) -> User:
        existing_user = await self._repository_user.exists(
            username=user_schema.username, email=user_schema.email
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username or email address is already taken'
            )

        return await self._repository_user.create_user(user_schema.model_dump())

    async def update(self, *, user_id: UUID, obj_in) -> User:
        return await self._repository_user.update(
            obj_id=user_id,
            obj_in=obj_in
        )

    async def list(self, *args, **kwargs) -> list[User]:
        return await self._repository_user.list(*args, **kwargs)

    async def delete(self, obj_id: UUID) -> None:
        return await self._repository_user.delete(obj_id=obj_id)

    async def exists(self, *args, **kwargs) -> User | None:
        return await self._repository_user.exists(*args, **kwargs)

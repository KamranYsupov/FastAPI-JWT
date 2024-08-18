from typing import TypeVar

from .base import RepositoryBase
from app.db import User
from ..utils.hashers import hash_password

ModelType = TypeVar("ModelType")


class RepositoryUser(RepositoryBase[User]):
    """Репозиторий для работы с таблицей users"""

    async def create_user(self, obj_in) -> ModelType:
        obj_in_data = dict(obj_in)
        hashed_password = hash_password(obj_in_data['password'])
        obj_in_data['password'] = hashed_password

        return await self.create(obj_in=obj_in_data)



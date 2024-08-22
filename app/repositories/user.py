from .base import RepositoryBase
from app.db import User
from ..utils.hashers import hash_password


class RepositoryUser(RepositoryBase[User]):
    """Репозиторий для работы с таблицей users"""
    
    async def get(
        self, 
        join_seller: bool = False,
        **kwargs,
    ) -> User | None:
        if not join_seller:
            return await super().get(**kwargs)

        statement = select(User).options(joininload(User.seller)).filter_by(**kwargs)
        result = await self._session.execute(statement)
        return result.scalars().first()

    async def create_user(
        self, 
        obj_in,
        unique_fields: list[str] | tuple[str] | None = None,
    ) -> User:
        obj_in_data = dict(obj_in)
        hashed_password = hash_password(obj_in_data['password'])
        obj_in_data['password'] = hashed_password

        return await super().create(
            obj_in=obj_in_data,
            unique_fields=unique_fields
        )

    
    




from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .base import RepositoryBase
from app.db import User


class RepositoryUser(RepositoryBase[User]):
    """Репозиторий для работы с таблицей users"""
    
    async def get(
        self, 
        join_seller: bool = False,
        **kwargs,
    ) -> User | None:
        if not join_seller:
            return await super().get(**kwargs)

        statement = select(User).options(joinedload(User.seller)).filter_by(**kwargs)
        result = await self._session.execute(statement)
        return result.scalars().first()
        

    
    




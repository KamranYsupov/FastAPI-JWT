from uuid import UUID
from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar("ModelType")


class RepositoryBase(Generic[ModelType,]):
    """Репозиторий с базовым CRUD"""

    def __init__(
            self,
            model: Type[ModelType],
            session: AsyncSession,
    ) -> None:
        self._session = session
        self._model = model

    async def create(self, obj_in) -> ModelType:
        obj_in_data = dict(obj_in)
        db_obj = self._model(**obj_in_data)

        self._session.add(db_obj)
        await self._session.flush()
        await self._session.commit()

        return db_obj

    async def get(self, **kwargs) -> Optional[ModelType]:
        statement = select(self._model).filter_by(**kwargs)
        result = await self._session.execute(statement)
        return result.scalars().first()

    async def list(self, *args, **kwargs):
        statement = select(self._model).filter(*args).filter_by(**kwargs)
        result = await self._session.execute(statement)
        return result.scalars().all()

    async def update(
            self,
            *,
            obj_id: UUID,
            obj_in
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump()

        statement = (
            update(self._model).
            where(self._model.id == obj_id).
            values(**update_data)
        )
        await self._session.execute(statement)
        await self._session.commit()

        return await self._session.get(self._model, obj_id)

    async def delete(self, obj_id: UUID) -> None:
        statement = delete(self._model).where(self._model.id == obj_id)
        await self._session.execute(statement)

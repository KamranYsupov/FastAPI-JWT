from uuid import UUID
from typing import (
    Generic,
    Optional,
    Type,
    TypeVar,
    List,
    Tuple
)

from sqlalchemy import select, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.exceptions import AlreadyExistsError

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

    async def create(
            self, 
            obj_in,
            unique_fields: List[str] | Tuple[str] | None = None
    ) -> ModelType:
        
        if isinstance(obj_in, dict):
            insert_data = obj_in
        else:
            insert_data = obj_in.model_dump()
        
        if unique_fields:
            await self.check_unique_fields(
                insert_data=insert_data, unique_fields=unique_fields
            )
            
        db_obj = self._model(**insert_data)

        self._session.add(db_obj)
        await self._session.commit()
        await self._session.refresh(db_obj)

        return db_obj

    async def get(self, **kwargs) -> Optional[ModelType]:
        statement = select(self._model).filter_by(**kwargs)
        result = await self._session.execute(statement)
        return result.scalars().first()
    
    async def update(
            self,
            *,
            obj_id: UUID,
            obj_in,
            unique_fields: List[str] | Tuple[str] | None = None
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump()
            
        if unique_fields:
            await self.check_unique_fields(
                insert_data=update_data, unique_fields=unique_fields
            )
            
        statement = (
            update(self._model).
            where(self._model.id == obj_id).
            values(**update_data)
        )
        await self._session.execute(statement)
        await self._session.commit()

        return await self._session.get(self._model, obj_id)


    async def list(self, *args, **kwargs):
        statement = select(self._model).filter(*args).filter_by(**kwargs)
        result = await self._session.execute(statement)
        return result.scalars().all()

    async def delete(self, **kwargs) -> None:
        statement = delete(self._model).filter_by(**kwargs)
        await self._session.execute(statement)

    async def exists(self, *args, **kwargs) -> ModelType | None:
        statement = select(self._model).filter(or_(*args)).filter_by(**kwargs)
        result = await self._session.execute(statement)
        return result.scalars().one_or_none()
    
    async def check_unique_fields(
            self, 
            insert_data: dict,
            unique_fields: List[str] | Tuple[str] | None = None,
    ) -> bool:
        if unique_fields:
            unique_kwargs = {
                field: insert_data.get(field) for field in unique_fields
            }
            conditions: List[bool] = [
                getattr(self._model, field) == value 
                for field, value in unique_kwargs.items()
            ]
            
            existing_obj = await self.exists(*conditions)
            
            
        if existing_obj:
            formatted_fields_string = ' or '.join(unique_fields).capitalize()
            
            raise AlreadyExistsError(
                f'{formatted_fields_string} is already taken'
            )
            
        return True


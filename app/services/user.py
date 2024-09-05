from typing import List, Tuple


from app.db import User
from app.utils.hashers import hash_password
from .mixins import CRUDServiceMixin
from app.repositories.user import RepositoryUser



class UserService(CRUDServiceMixin):
    def __init__(
        self,
        repository_user: RepositoryUser,
        unique_fields: List[str] | Tuple[str] | None = None,
    ):
        self._repository_user = repository_user
        super().__init__(
            repository=repository_user,
            unique_fields=unique_fields,
        )
        
    async def get(
        self, 
        join_seller: bool = False,
        **kwargs,
    ) -> User | None:
        return await self._repository_user.get(
            join_seller=join_seller,
            **kwargs,
        )
        
    async def create_user(self, obj_in): 
        obj_in_data = dict(obj_in)
        hashed_password = hash_password(obj_in_data['password'])
        obj_in_data['password'] = hashed_password

        return await super().create(
            obj_in=obj_in_data,
        )
        

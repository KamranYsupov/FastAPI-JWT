import uuid

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.schemas.mixins import UserSchemaMixin





class UserSchema(UserSchemaMixin):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID


class CreateUserSchema(UserSchemaMixin):
    password: str = Field(title='Пароль', min_length=8)





import uuid

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserSchemaMixin(BaseModel):
    username: str = Field(title='Имя пользователя', max_length=50, min_length=8)
    email: EmailStr = Field(title='E-mail')


class UserSchema(UserSchemaMixin):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID


class CreateUserSchema(UserSchemaMixin):
    password: str = Field(title='Пароль', min_length=8)





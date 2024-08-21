import uuid

import jwt
from jwt.exceptions import InvalidTokenError
from dependency_injector.wiring import inject, Provide
from fastapi import HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from starlette import status

from app.core.config import settings
from app.core.container import Container
from app.db import User
from app.schemas.auth import AuthUserSchema
from app.services.jwt import JWTService, TokenEnum
from app.services.user import UserService
from app.utils.hashers import check_password

http_bearer = HTTPBearer()


@inject
async def get_current_jwt_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        jwt_service: JWTService = Depends(Provide[Container.jwt_service])
) -> dict:
    token = credentials.credentials
    return await jwt_service.decode(token=token)


@inject
async def get_current_payload_user(
        payload: dict = Depends(get_current_jwt_payload),
        user_service: UserService = Depends(Provide[Container.user_service])
) -> User:
    if not (user := await user_service.get(id=uuid.UUID(payload.get('sub')))):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return user


class AuthUserFromToken:
    """
    Класс для создания зависимостей текущего пользователя
    по access и refresh токенам,
     с целью аутентификации, выпуска и обновления access токена
    """

    def __init__(self, token_type: TokenEnum):
        self.token_type = token_type

    async def __call__(self, payload: dict = Depends(get_current_jwt_payload)) -> User:
        self.validate_token(payload, expected_token_type=self.token_type)
        user = await get_current_payload_user(payload)
        return user

    @staticmethod
    def validate_token(payload: dict, expected_token_type: TokenEnum) -> bool:
        current_token_type = payload.get('type')
        if current_token_type != expected_token_type.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'expected {expected_token_type.value!r} token but got {current_token_type!r}'
            )

        return True


get_current_user_access = AuthUserFromToken(token_type=TokenEnum.ACCESS)
get_current_user_refresh = AuthUserFromToken(token_type=TokenEnum.REFRESH)


@inject
async def validate_auth_user(
        auth_user_schema: AuthUserSchema,
        user_service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    unauthentic_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password'
    )
    if not (user := await user_service.get(username=auth_user_schema.username)):
        raise unauthentic_exception

    if not check_password(user.password, auth_user_schema.password):
        raise unauthentic_exception

    return user

import datetime
import enum

import jwt

from app.core.config import settings
from app.db import User
from app.schemas.user import UserSchema


class TokenEnum(enum.Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'


class JWTService:
    def __init__(
            self,
            algorithm: str = settings.algorithm,
            access_expire_minutes: int = settings.access_expire_minutes,
            refresh_expire_days: int = settings.refresh_expire_days,
    ):
        self.algorithm = algorithm
        self.access_expire_minutes = access_expire_minutes
        self.refresh_expire_days = refresh_expire_days

    def encode(self, user: User | UserSchema, token_type: TokenEnum) -> str:
        payload = {'sub': str(user.id)}
        now = datetime.datetime.utcnow()
        if token_type == TokenEnum.ACCESS:
            timedelta = datetime.timedelta(minutes=self.access_expire_minutes)
            payload.update(username=user.username, email=user.email)

        elif token_type == TokenEnum.REFRESH:
            timedelta = datetime.timedelta(days=self.refresh_expire_days)

        else:
            raise AttributeError('invalid token_type')

        expire = now + timedelta

        payload.update(type=token_type.value, exp=expire, iat=now)
        token = jwt.encode(
            payload=payload,
            key=settings.secret_key,
            algorithm=self.algorithm
        )

        return token

    def decode(self, token: str | bytes):
        payload = jwt.decode(
            token,
            algorithms=[self.algorithm],
            options={'verify_signature': False}
        )
        return payload

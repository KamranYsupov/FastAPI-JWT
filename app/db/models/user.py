from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampedMixin


class User(Base, TimestampedMixin):
    """Модель пользователя"""
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[bytes]

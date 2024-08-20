import uuid
from datetime import datetime

from sqlalchemy import func, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from app.core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.metadata_naming_convention
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )


class AbstractUser(Base):
    """Абстрактная модель пользователя"""

    __abstract__ = True

    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[bytes]


class TimestampedMixin:
    """Миксин для даты создания и даты обновления"""

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

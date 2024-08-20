from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_mixins import AbstractUser, TimestampedMixin


if TYPE_CHECKING:
    from .seller import Seller


class User(AbstractUser, TimestampedMixin):
    """Модель пользователя"""

    bill: Mapped[float] = mapped_column(default=0)

    seller: Mapped['Seller'] = relationship(back_populates='user')

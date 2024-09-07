from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_mixins import Base, TimestampedMixin


if TYPE_CHECKING:
    from .user import User
    from .product import Product


class Seller(Base, TimestampedMixin):
    """Модель продавца"""

    name: Mapped[str] = mapped_column(String(32), unique=True)
    bio: Mapped[str | None]
    is_verified: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        unique=True,
    )

    user: Mapped['User'] = relationship(back_populates='seller')
    products: Mapped[list['Product']] = relationship(
        back_populates='seller', 
        lazy='selectin',
    )


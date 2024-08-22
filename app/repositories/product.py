from .base import RepositoryBase
from app.db import Product


class RepositoryProduct(RepositoryBase[Product]):
    """Репозиторий для работы с таблицей products"""
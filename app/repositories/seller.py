from .base import RepositoryBase
from app.db import Seller


class RepositorySeller(RepositoryBase[Seller]):
    """Репозиторий для работы с таблицей sellers"""
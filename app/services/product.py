from typing import List, Tuple

from .mixins import CRUDServiceMixin
from app.repositories import RepositoryProduct


class ProductService(CRUDServiceMixin):
    def __init__(
        self, 
        repository_product: RepositoryProduct,
        unique_fields: List[str] | Tuple[str] | None = None,
    ):
        self._repository_product = repository_product
        super().__init__(
            repository=repository_product,
            unique_fields=unique_fields,
        )
           

    
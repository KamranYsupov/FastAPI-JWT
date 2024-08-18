from dependency_injector import containers, providers

from app.repositories.user import RepositoryUser
from app.core.config import settings
from app.db import DataBaseManager, User
from app.services.user import UserService
from app.services.jwt import JWTService


class Container(containers.DeclarativeContainer):
    db_manager = providers.Singleton(DataBaseManager, db_url=settings.db_url)
    session = providers.Resource(db_manager().get_async_session)

    # region repository
    repository_user = providers.Singleton(
        RepositoryUser, model=User, session=session
    )
    # endregion

    # region services
    user_service = providers.Singleton(
        UserService, repository_user=repository_user
    )
    jwt_service = providers.Singleton(JWTService)
    # endregion


container = Container()
container.wire(modules=settings.container_wiring_modules)

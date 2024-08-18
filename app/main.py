from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.core.container import Container, container
from app.api.v1 import routers
from app.db import Base, db_manager


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


def create_app() -> FastAPI:
    fastapi_app = FastAPI(
        title=settings.project_name,
        lifespan=lifespan,
    )

    fastapi_app.container = container
    fastapi_app.include_router(routers.api_router, prefix=settings.api_v1_prefix)
    return fastapi_app


app = create_app()


if __name__ == '__main__':
    uvicorn.run(app='app.main:app', reload=True)

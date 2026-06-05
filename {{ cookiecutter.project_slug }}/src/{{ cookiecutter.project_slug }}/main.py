from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from loguru import logger

from .api import router
from .infra import engine, logging, middleware, response, settings


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    logger.patch(logging.source("", "")).info("Listening at http://{}:{}", settings.app_host, settings.app_port)
    await engine.init_db()
    yield
    await engine.db_engine.dispose()


def init_middlewares(asgi_app: FastAPI) -> None:
    middleware.cors.add_middleware(asgi_app)
    middleware.error.add_middleware(asgi_app)
    middleware.error.add_exception_handler(asgi_app)


def init_routes(asgi_app: FastAPI) -> None:
    asgi_app.include_router(router)


def create_app() -> FastAPI:
    logging.init_logger()
    openapi_url = "/openapi.json" if settings.app_debug else None
    asgi_app = FastAPI(
        title="{{ cookiecutter.project_name }}",
        version="{{ cookiecutter.project_version }}",
        lifespan=lifespan,
        openapi_url=openapi_url,
    )

    @asgi_app.get("/")
    async def root() -> response.AppResponse[dict]:
        return response.ResponseHandler.success({"message": "Welcome to {{ cookiecutter.project_name }}"})

    init_middlewares(asgi_app)
    init_routes(asgi_app)
    return asgi_app


asgi_app = create_app()

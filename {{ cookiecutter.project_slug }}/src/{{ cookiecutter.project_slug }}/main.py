from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from loguru import logger

from {{ cookiecutter.project_slug }}.api.middleware import cors, error
from {{ cookiecutter.project_slug }}.api.router import router as api_router
from {{ cookiecutter.project_slug }}.infra import engine
from {{ cookiecutter.project_slug }}.infra import logging as app_logging
from {{ cookiecutter.project_slug }}.infra.settings import settings

app_logging.init_logger()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    logger.patch(app_logging.source("", "")).info(
        "Listening at http://{}:{}", settings.app_host, settings.app_port
    )
    await engine.init_db()
    yield
    await engine.db_engine.dispose()


def init_middlewares(asgi_app: FastAPI) -> None:
    cors.add_middleware(asgi_app)
    error.add_middleware(asgi_app)
    error.add_exception_handler(asgi_app)


def init_routes(asgi_app: FastAPI) -> None:
    asgi_app.include_router(api_router)


def create_app() -> FastAPI:
    openapi_url = "/openapi.json" if settings.app_debug else None
    asgi_app = FastAPI(
        title="{{ cookiecutter.project_name }}",
        version="{{ cookiecutter.project_version }}",
        lifespan=lifespan,
        openapi_url=openapi_url,
    )

    @asgi_app.get("/")
    async def root():
        return {"message": "Welcome to {{ cookiecutter.project_name }}"}

    init_middlewares(asgi_app)
    init_routes(asgi_app)
    return asgi_app


asgi_app = create_app()

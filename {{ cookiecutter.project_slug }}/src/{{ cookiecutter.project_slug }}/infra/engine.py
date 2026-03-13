import json
from collections.abc import AsyncIterator

from alembic.config import Config as AlembicConfig
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from alembic import command
from {{ cookiecutter.project_slug }}.infra import logging as app_logging
from {{ cookiecutter.project_slug }}.infra.settings import settings


def _create_engine() -> AsyncEngine:
    kwargs: dict = {
        "future": True,
        "json_serializer": lambda val: json.dumps(val, ensure_ascii=False, default=str),
    }
    if "aiosqlite" not in settings.database_url:
        kwargs.update({"pool_size": 20, "pool_pre_ping": True, "pool_recycle": 3600, "max_overflow": 30})
    return create_async_engine(settings.database_url, **kwargs)


db_engine: AsyncEngine = _create_engine()
db_session = async_sessionmaker(bind=db_engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with db_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def init_db(skip_migration: bool = False) -> None:
    def _execute_upgrade(connection):
        cfg = AlembicConfig(config_args={"script_location": "alembic"})
        cfg.attributes["connection"] = connection
        command.upgrade(cfg, "head")

    try:
        if not skip_migration:
            async with db_engine.begin() as conn:
                await conn.run_sync(_execute_upgrade)
        logger.patch(app_logging.source()).info("Database ready at {}", settings.database_url)
    except (SQLAlchemyError, OSError):
        logger.patch(app_logging.source()).error("Failed to connect to database at {}", settings.database_url)

import json
from collections.abc import AsyncIterator

from alembic.config import Config as AlembicConfig
from loguru import logger
from sqlalchemy.engine.base import Connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from alembic import command
from fastapi_perfectionist_starter.infra import logging
from fastapi_perfectionist_starter.infra.settings import settings


def _create_engine() -> AsyncEngine:
    in_sqlite = "aiosqlite" in settings.database_url
    connection_pool_kwargs: dict = {"pool_size": 20, "pool_pre_ping": True, "pool_recycle": 3600, "max_overflow": 30}

    return create_async_engine(
        settings.database_url,
        **{
            "future": True,
            "json_serializer": lambda val: json.dumps(val, ensure_ascii=False, default=str),
            **({} if in_sqlite else connection_pool_kwargs),
        },
    )


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
    def _execute_upgrade(connection: Connection) -> None:
        cfg = AlembicConfig(config_args={"script_location": "alembic"})
        cfg.attributes["connection"] = connection
        command.upgrade(cfg, "head")

    try:
        if not skip_migration:
            async with db_engine.begin() as conn:
                await conn.run_sync(_execute_upgrade)
        logger.patch(logging.source()).info("数据库已就绪：{}", settings.database_url)
    except (SQLAlchemyError, OSError) as _:
        logger.patch(logging.source()).exception("无法连接到数据库：{}", settings.database_url)

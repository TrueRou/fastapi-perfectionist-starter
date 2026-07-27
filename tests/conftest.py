from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from fastapi_perfectionist_starter.infra.models import DbBase, Note, User
from fastapi_perfectionist_starter.modules.note.services import NoteService
from fastapi_perfectionist_starter.modules.user.services import UserService
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


@pytest_asyncio.fixture(scope="function")
async def engine() -> AsyncIterator[AsyncEngine]:
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    async with test_engine.begin() as conn:
        await conn.run_sync(DbBase.metadata.create_all)
    yield test_engine
    async with test_engine.begin() as conn:
        await conn.run_sync(DbBase.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture()
async def session(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with SessionLocal() as session, session.begin():
        yield session
        await session.rollback()


@pytest.fixture()
def user_service(session: AsyncSession) -> UserService:
    return UserService(session)


@pytest.fixture()
def note_service(session: AsyncSession) -> NoteService:
    return NoteService(session)


@pytest_asyncio.fixture()
async def sample_user(user_service: UserService) -> User:
    return await user_service.create_user("testuser", "test@example.com", "testpass123")


@pytest_asyncio.fixture()
async def sample_note(note_service: NoteService, sample_user: User) -> Note:
    return await note_service.create_note(sample_user.id, "Test Note", "This is a test note.")

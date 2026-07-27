import uuid
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_perfectionist_starter.infra import engine, models, pagination


class NoteService:
    def __init__(self, session: Annotated[AsyncSession, Depends(engine.get_db)]) -> None:
        self.session = session

    async def create_note(self, user_id: uuid.UUID, title: str, content: str) -> models.Note:
        note = models.Note(title=title, content=content, user_id=user_id)
        self.session.add(note)
        await self.session.flush()
        return note

    async def get_note(self, note_id: uuid.UUID) -> models.Note | None:
        return await self.session.get(models.Note, note_id)

    async def list_notes(self, user_id: uuid.UUID, params: pagination.PaginationParams) -> pagination.Page[models.Note]:
        query = select(models.Note).where(models.Note.user_id == user_id).order_by(models.Note.created_at.desc())
        return await pagination.paginate(self.session, query, params)

    async def update_note(self, note: models.Note, title: str | None = None, content: str | None = None) -> models.Note:
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        note.updated_at = datetime.now(UTC)
        await self.session.flush()
        return note

    async def delete_note(self, note: models.Note) -> None:
        await self.session.delete(note)
        await self.session.flush()

import uuid
from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from {{ cookiecutter.project_slug }}.infra import engine, models, pagination


class NoteService:
    def __init__(self, session: Annotated[AsyncSession, Depends(engine.get_db)]):
        self.session = session

    async def create_note(self, user_id: uuid.UUID, title: str, content: str) -> models.Note:
        note = models.Note(title=title, content=content, user_id=user_id)
        self.session.add(note)
        await self.session.flush([note])
        return note

    async def get_note(self, note_id: uuid.UUID) -> models.Note | None:
        return await self.session.get(models.Note, note_id)

    async def list_notes(self, user_id: uuid.UUID, params: pagination.PaginationParams) -> pagination.Page[models.Note]:
        query = (
            select(models.Note).where(col(models.Note.user_id) == user_id).order_by(col(models.Note.created_at).desc())
        )
        return await pagination.paginate(self.session, query, params)

    async def update_note(self, note: models.Note, title: str | None = None, content: str | None = None) -> models.Note:
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        note.updated_at = datetime.utcnow()
        await self.session.flush([note])
        return note

    async def delete_note(self, note: models.Note) -> None:
        await self.session.delete(note)
        await self.session.flush()

    async def require_note(self, note_id: uuid.UUID, user_id: uuid.UUID) -> models.Note:
        note = await self.get_note(note_id)
        if note is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        if note.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return note

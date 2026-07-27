import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status

from fastapi_perfectionist_starter.infra import models
from fastapi_perfectionist_starter.modules.auth.dependencies import RequireAuthUser
from fastapi_perfectionist_starter.modules.note.services import NoteService


class RequireNote:
    async def __call__(
        self,
        note_id: uuid.UUID,
        dep_user: Annotated[models.User, Depends(RequireAuthUser())],
        srv_note: Annotated[NoteService, Depends()],
    ) -> models.Note:
        note = await srv_note.get_note(note_id)
        if note is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="笔记不存在")
        if note.user_id != dep_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权访问此笔记")
        return note

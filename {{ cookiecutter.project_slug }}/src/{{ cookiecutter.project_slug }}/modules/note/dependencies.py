import uuid
from typing import Annotated

from fastapi import Depends

from {{ cookiecutter.project_slug }}.infra import models
from {{ cookiecutter.project_slug }}.modules.note import NoteService
from {{ cookiecutter.project_slug }}.modules.user import RequireUser


class RequireNote:
    async def __call__(
        self,
        note_id: uuid.UUID,
        dep_user: Annotated[models.User, Depends(RequireUser())],
        srv_note: Annotated[NoteService, Depends()],
    ) -> models.Note:
        return await srv_note.require_note(note_id, dep_user.id)

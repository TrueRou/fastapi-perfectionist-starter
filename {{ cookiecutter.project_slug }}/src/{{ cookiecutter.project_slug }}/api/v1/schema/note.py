import uuid
from datetime import datetime

from pydantic import Field

from {{ cookiecutter.project_slug }}.infra import models


class NotePublic(models.BaseModel):
    id: uuid.UUID
    title: str
    content: str
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class NoteCreateRequest(models.BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class NoteUpdateRequest(models.BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = Field(None, min_length=1)

import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query

from {{ cookiecutter.project_slug }}.api.schema.note import NoteCreateRequest, NotePublic, NoteUpdateRequest
from {{ cookiecutter.project_slug }}.infra.models import Note, User
from {{ cookiecutter.project_slug }}.infra.pagination import Page, PaginationParams
from {{ cookiecutter.project_slug }}.infra.response import AppResponse, ResponseHandler
from {{ cookiecutter.project_slug }}.modules.note.services import NoteService
from {{ cookiecutter.project_slug }}.modules.user.dependencies import RequireUser

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=AppResponse[NotePublic])
async def create_note(
    body: Annotated[NoteCreateRequest, Body()],
    dep_user: Annotated[User, Depends(RequireUser())],
    srv_note: Annotated[NoteService, Depends()],
):
    note = await srv_note.create_note(dep_user.id, body.title, body.content)
    return ResponseHandler.success(note)


@router.get("", response_model=AppResponse[Page[NotePublic]])
async def list_notes(
    dep_user: Annotated[User, Depends(RequireUser())],
    srv_note: Annotated[NoteService, Depends()],
    params: Annotated[PaginationParams, Query()],
):
    page = await srv_note.list_notes(dep_user.id, params)
    return ResponseHandler.success(page)


@router.get("/{note_id}", response_model=AppResponse[NotePublic])
async def get_note(
    note_id: uuid.UUID,
    dep_user: Annotated[User, Depends(RequireUser())],
    srv_note: Annotated[NoteService, Depends()],
):
    note = await srv_note.require_note(note_id, dep_user.id)
    return ResponseHandler.success(note)


@router.patch("/{note_id}", response_model=AppResponse[NotePublic])
async def update_note(
    note_id: uuid.UUID,
    body: Annotated[NoteUpdateRequest, Body()],
    dep_user: Annotated[User, Depends(RequireUser())],
    srv_note: Annotated[NoteService, Depends()],
):
    note = await srv_note.require_note(note_id, dep_user.id)
    updated = await srv_note.update_note(note, body.title, body.content)
    return ResponseHandler.success(updated)


@router.delete("/{note_id}", response_model=AppResponse[None])
async def delete_note(
    note_id: uuid.UUID,
    dep_user: Annotated[User, Depends(RequireUser())],
    srv_note: Annotated[NoteService, Depends()],
):
    note = await srv_note.require_note(note_id, dep_user.id)
    await srv_note.delete_note(note)
    return ResponseHandler.success(None)

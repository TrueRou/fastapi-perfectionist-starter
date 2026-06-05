from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query

from {{ cookiecutter.project_slug }}.infra import models, pagination, response
from {{ cookiecutter.project_slug }}.modules.note import NoteService, RequireNote
from {{ cookiecutter.project_slug }}.modules.user import RequireUser

from .schema.note import NoteCreateRequest, NotePublic, NoteUpdateRequest

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=response.AppResponse[NotePublic])
async def create_note(
    body: Annotated[NoteCreateRequest, Body()],
    dep_user: Annotated[models.User, Depends(RequireUser())],
    srv_note: Annotated[NoteService, Depends()],
):
    note = await srv_note.create_note(dep_user.id, body.title, body.content)
    return response.ResponseHandler.success(note)


@router.get("", response_model=response.AppResponse[pagination.Page[NotePublic]])
async def list_notes(
    dep_user: Annotated[models.User, Depends(RequireUser())],
    srv_note: Annotated[NoteService, Depends()],
    params: Annotated[pagination.PaginationParams, Query()],
):
    page = await srv_note.list_notes(dep_user.id, params)
    return response.ResponseHandler.success(page)


@router.get("/{note_id}", response_model=response.AppResponse[NotePublic])
async def get_note(
    dep_note: Annotated[models.Note, Depends(RequireNote())],
):
    return response.ResponseHandler.success(dep_note)


@router.patch("/{note_id}", response_model=response.AppResponse[NotePublic])
async def update_note(
    body: Annotated[NoteUpdateRequest, Body()],
    dep_note: Annotated[models.Note, Depends(RequireNote())],
    srv_note: Annotated[NoteService, Depends()],
):
    updated = await srv_note.update_note(dep_note, body.title, body.content)
    return response.ResponseHandler.success(updated)


@router.delete("/{note_id}", response_model=response.AppResponse[None])
async def delete_note(
    dep_note: Annotated[models.Note, Depends(RequireNote())],
    srv_note: Annotated[NoteService, Depends()],
):
    await srv_note.delete_note(dep_note)
    return response.ResponseHandler.success(None)

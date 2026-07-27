from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query

from fastapi_perfectionist_starter.api.v1.schema.note import NoteCreateRequest, NoteResponse, NoteUpdateRequest
from fastapi_perfectionist_starter.infra import models, pagination, response
from fastapi_perfectionist_starter.modules.auth.dependencies import RequireAuthUser
from fastapi_perfectionist_starter.modules.note.dependencies import RequireNote
from fastapi_perfectionist_starter.modules.note.services import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=response.AppResponse[NoteResponse])
async def create_note(
    body: Annotated[NoteCreateRequest, Body()],
    dep_user: Annotated[models.User, Depends(RequireAuthUser())],
    srv_note: Annotated[NoteService, Depends()],
) -> response.AppResponse[models.Note]:
    note = await srv_note.create_note(dep_user.id, body.title, body.content)
    return response.ResponseHandler.success(note)


@router.get("", response_model=response.AppResponse[pagination.Page[NoteResponse]])
async def list_notes(
    dep_user: Annotated[models.User, Depends(RequireAuthUser())],
    srv_note: Annotated[NoteService, Depends()],
    params: Annotated[pagination.PaginationParams, Query()],
) -> response.AppResponse[pagination.Page[models.Note]]:
    page = await srv_note.list_notes(dep_user.id, params)
    return response.ResponseHandler.success(page)


@router.get("/{note_id}", response_model=response.AppResponse[NoteResponse])
async def get_note(
    dep_note: Annotated[models.Note, Depends(RequireNote())],
) -> response.AppResponse[models.Note]:
    return response.ResponseHandler.success(dep_note)


@router.patch("/{note_id}", response_model=response.AppResponse[NoteResponse])
async def update_note(
    body: Annotated[NoteUpdateRequest, Body()],
    dep_note: Annotated[models.Note, Depends(RequireNote())],
    srv_note: Annotated[NoteService, Depends()],
) -> response.AppResponse[models.Note]:
    updated = await srv_note.update_note(dep_note, body.title, body.content)
    return response.ResponseHandler.success(updated)


@router.delete("/{note_id}", response_model=response.AppResponse[None])
async def delete_note(
    dep_note: Annotated[models.Note, Depends(RequireNote())],
    srv_note: Annotated[NoteService, Depends()],
) -> response.AppResponse[None]:
    await srv_note.delete_note(dep_note)
    return response.ResponseHandler.success(None)

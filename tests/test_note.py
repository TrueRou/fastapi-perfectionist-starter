import uuid

import pytest
from fastapi import HTTPException
from fastapi_perfectionist_starter.infra.models import Note, User
from fastapi_perfectionist_starter.infra.pagination import PaginationParams
from fastapi_perfectionist_starter.modules.note.services import NoteService
from fastapi_perfectionist_starter.modules.user.services import UserService


class TestNoteCreate:
    async def test_create_note_success(self, note_service: NoteService, sample_user: User) -> None:
        note = await note_service.create_note(sample_user.id, "My Note", "Content here.")
        assert note.title == "My Note"
        assert note.content == "Content here."
        assert note.user_id == sample_user.id

    async def test_create_note_user_ownership(self, note_service: NoteService, user_service: UserService) -> None:
        user_a = await user_service.create_user("alice", "alice@example.com", "password123")
        user_b = await user_service.create_user("bob", "bob@example.com", "password123")

        note_a = await note_service.create_note(user_a.id, "Alice's note", "only alice's")
        note_b = await note_service.create_note(user_b.id, "Bob's note", "only bob's")

        assert note_a.user_id == user_a.id
        assert note_b.user_id == user_b.id


class TestNoteCRUD:
    async def test_list_notes_pagination(self, note_service: NoteService, sample_user: User) -> None:
        for i in range(3):
            await note_service.create_note(sample_user.id, f"Note {i}", f"Content {i}")

        page = await note_service.list_notes(sample_user.id, PaginationParams(page_number=1, page_size=2))
        assert page.total_row == 3
        assert len(page.records) == 2

    async def test_get_note_by_id(self, note_service: NoteService, sample_note: Note) -> None:
        fetched = await note_service.get_note(sample_note.id)
        assert fetched is not None
        assert fetched.id == sample_note.id

    async def test_update_note_partial(self, note_service: NoteService, sample_note: Note) -> None:
        updated = await note_service.update_note(sample_note, title="New Title")
        assert updated.title == "New Title"
        assert updated.content == sample_note.content

    async def test_delete_note(self, note_service: NoteService, sample_note: Note) -> None:
        await note_service.delete_note(sample_note)
        result = await note_service.get_note(sample_note.id)
        assert result is None

    async def test_require_note_wrong_user(
        self,
        note_service: NoteService,
        user_service: UserService,
        sample_note: Note,
    ) -> None:
        other_user = await user_service.create_user("other", "other@example.com", "password123")
        with pytest.raises(HTTPException) as exc_info:
            await note_service.require_note(sample_note.id, other_user.id)
        assert exc_info.value.status_code == 403

    async def test_require_note_not_found(self, note_service: NoteService, sample_user: User) -> None:
        with pytest.raises(HTTPException) as exc_info:
            await note_service.require_note(uuid.uuid4(), sample_user.id)
        assert exc_info.value.status_code == 404

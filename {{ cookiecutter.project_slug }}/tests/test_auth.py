import pytest
import jwt as pyjwt

from {{ cookiecutter.project_slug }}.infra.settings import settings
from {{ cookiecutter.project_slug }}.modules.user.services import UserService


class TestUserCreate:
    async def test_create_user_success(self, user_service: UserService):
        user = await user_service.create_user("alice", "alice@example.com", "password123")
        assert user.username == "alice"
        assert user.email == "alice@example.com"
        assert user.hashed_password != "password123"

    async def test_create_user_duplicate_username(self, user_service: UserService, sample_user):
        with pytest.raises(Exception) as exc_info:
            await user_service.create_user("testuser", "other@example.com", "password123")
        assert exc_info.value.status_code == 400

    async def test_create_user_duplicate_email(self, user_service: UserService, sample_user):
        with pytest.raises(Exception) as exc_info:
            await user_service.create_user("otheruser", "test@example.com", "password123")
        assert exc_info.value.status_code == 400


class TestUserAuthentication:
    async def test_auth_by_username(self, user_service: UserService, sample_user):
        user = await user_service.auth_user("testuser", "testpass123")
        assert user.id == sample_user.id

    async def test_auth_by_email(self, user_service: UserService, sample_user):
        user = await user_service.auth_user("test@example.com", "testpass123")
        assert user.id == sample_user.id

    async def test_auth_wrong_password(self, user_service: UserService, sample_user):
        with pytest.raises(Exception) as exc_info:
            await user_service.auth_user("testuser", "wrongpassword")
        assert exc_info.value.status_code == 401

    async def test_auth_nonexistent_user(self, user_service: UserService):
        with pytest.raises(Exception) as exc_info:
            await user_service.auth_user("nobody", "password123")
        assert exc_info.value.status_code == 401


class TestUserTokens:
    async def test_generate_token(self, user_service: UserService, sample_user):
        token = user_service.generate_token(sample_user)
        payload = pyjwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        assert payload["sub"] == str(sample_user.id)

    async def test_verify_token_round_trip(self, user_service: UserService, sample_user):
        token = user_service.generate_token(sample_user)
        payload = user_service.verify_token(token)
        assert payload["sub"] == str(sample_user.id)

    async def test_verify_expired_token(self, user_service: UserService, sample_user):
        from datetime import datetime, timedelta, timezone

        from freezegun import freeze_time

        token = user_service.generate_token(sample_user)

        future = datetime.now(timezone.utc) + timedelta(days=settings.jwt_expiration_days + 1)
        with freeze_time(future):
            with pytest.raises(Exception) as exc_info:
                user_service.verify_token(token)
            assert exc_info.value.status_code == 401
            assert "expired" in exc_info.value.detail.lower()

    async def test_verify_invalid_token(self, user_service: UserService):
        with pytest.raises(Exception) as exc_info:
            user_service.verify_token("this.is.not.a.valid.token")
        assert exc_info.value.status_code == 401
        assert "invalid" in exc_info.value.detail.lower()

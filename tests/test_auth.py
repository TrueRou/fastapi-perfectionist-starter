from datetime import UTC

import jwt as pyjwt
import pytest
from fastapi import HTTPException

from fastapi_perfectionist_starter.infra.models import User
from fastapi_perfectionist_starter.infra.settings import settings
from fastapi_perfectionist_starter.modules.auth.services import AuthService
from fastapi_perfectionist_starter.modules.user.services import UserService


class TestUserCreate:
    async def test_create_user_success(self, user_service: UserService) -> None:
        user = await user_service.create_user("alice", "alice@example.com", "password123")
        assert user.username == "alice"
        assert user.email == "alice@example.com"
        assert user.hashed_password != "password123"

    async def test_create_user_duplicate_username(self, user_service: UserService, sample_user: User) -> None:
        with pytest.raises(HTTPException) as exc_info:
            await user_service.create_user("testuser", "other@example.com", "password123")
        assert exc_info.value.status_code == 400

    async def test_create_user_duplicate_email(self, user_service: UserService, sample_user: User) -> None:
        with pytest.raises(HTTPException) as exc_info:
            await user_service.create_user("otheruser", "test@example.com", "password123")
        assert exc_info.value.status_code == 400


class TestUserAuthentication:
    async def test_auth_by_username(self, auth_service: AuthService, sample_user: User) -> None:
        user = await auth_service.get_user("testuser", "testpass123")
        assert user.id == sample_user.id

    async def test_auth_by_email(self, auth_service: AuthService, sample_user: User) -> None:
        user = await auth_service.get_user("test@example.com", "testpass123")
        assert user.id == sample_user.id

    async def test_auth_wrong_password(self, auth_service: AuthService, sample_user: User) -> None:
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.get_user("testuser", "wrongpassword")
        assert exc_info.value.status_code == 401

    async def test_auth_nonexistent_user(self, auth_service: AuthService) -> None:
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.get_user("nobody", "password123")
        assert exc_info.value.status_code == 401


class TestUserTokens:
    async def test_generate_token(self, auth_service: AuthService, sample_user: User) -> None:
        token = auth_service.generate_token(sample_user)
        payload = pyjwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        assert payload["sub"] == str(sample_user.id)

    async def test_verify_token_round_trip(self, auth_service: AuthService, sample_user: User) -> None:
        token = auth_service.generate_token(sample_user)
        payload = auth_service.verify_token(token)
        assert payload["sub"] == str(sample_user.id)

    async def test_verify_expired_token(self, auth_service: AuthService, sample_user: User) -> None:
        from datetime import datetime, timedelta

        from freezegun import freeze_time

        token = auth_service.generate_token(sample_user)

        future = datetime.now(UTC) + timedelta(days=settings.jwt_expiration_days + 1)
        with freeze_time(future):
            with pytest.raises(HTTPException) as exc_info:
                auth_service.verify_token(token)
            assert exc_info.value.status_code == 401
            assert exc_info.value.detail == "令牌已过期"

    async def test_verify_invalid_token(self, auth_service: AuthService) -> None:
        with pytest.raises(HTTPException) as exc_info:
            auth_service.verify_token("this.is.not.a.valid.token")
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "无效的令牌"

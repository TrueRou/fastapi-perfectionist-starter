from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_perfectionist_starter.infra import engine, models
from fastapi_perfectionist_starter.infra.settings import settings
from fastapi_perfectionist_starter.modules.user.services import UserService


class AuthService:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(engine.get_db)],
        srv_user: Annotated[UserService, Depends()],
    ) -> None:
        self.session = session
        self.srv_user = srv_user
        self.hasher = PasswordHasher()

    async def get_user(self, username: str, password: str) -> models.User:
        clause = select(models.User.id).where(or_(models.User.username == username, models.User.email == username))
        user_id = (await self.session.execute(clause)).scalars().first()
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
            ) from None
        user = await self.srv_user.get_user(user_id)

        try:
            self.hasher.verify(user.hashed_password, password)
            return user
        except VerifyMismatchError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
            ) from e

    def generate_token(self, user: models.User) -> str:
        now = datetime.now(UTC)
        expires_at = now + timedelta(days=settings.jwt_expiration_days)
        payload = {"sub": str(user.id), "exp": int(expires_at.timestamp())}
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    def verify_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="令牌已过期") from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌") from e

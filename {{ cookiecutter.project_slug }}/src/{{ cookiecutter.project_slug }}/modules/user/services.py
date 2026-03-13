import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, HTTPException, status
from sqlmodel import col, or_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from {{ cookiecutter.project_slug }}.infra.engine import get_db
from {{ cookiecutter.project_slug }}.infra.models import User
from {{ cookiecutter.project_slug }}.infra.settings import settings as _default_settings


class UserService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_db)]):
        self.session = session
        self.hasher = PasswordHasher()
        self.settings = _default_settings

    async def create_user(self, username: str, email: str, password: str) -> User:
        clause = select(User).where(or_(col(User.username) == username, col(User.email) == email))
        if (await self.session.exec(clause)).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already taken")

        user = User(username=username, email=email, hashed_password=self.hasher.hash(password))
        self.session.add(user)
        await self.session.flush([user])
        return user

    async def auth_user(self, username: str, password: str) -> User:
        clause = select(User).where(or_(col(User.username) == username, col(User.email) == username))
        user = (await self.session.exec(clause)).first()
        try:
            if not user:
                raise VerifyMismatchError("not found")
            self.hasher.verify(user.hashed_password, password)
            return user
        except VerifyMismatchError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    async def get_user(self, user_id: uuid.UUID) -> User | None:
        return await self.session.get(User, user_id)

    def generate_token(self, user: User) -> str:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=self.settings.jwt_expiration_days)
        payload = {"sub": str(user.id), "exp": int(expires_at.timestamp())}
        return jwt.encode(payload, self.settings.jwt_secret, algorithm="HS256")

    def verify_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.settings.jwt_secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

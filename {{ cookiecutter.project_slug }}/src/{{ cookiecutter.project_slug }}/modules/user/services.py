import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, HTTPException, status
from sqlmodel import col, or_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from {{ cookiecutter.project_slug }}.infra import engine, models, settings


class UserService:
    def __init__(self, session: Annotated[AsyncSession, Depends(engine.get_db)]):
        self.session = session
        self.hasher = PasswordHasher()

    async def create_user(self, username: str, email: str, password: str) -> models.User:
        clause = select(models.User).where(or_(col(models.User.username) == username, col(models.User.email) == email))
        if (await self.session.exec(clause)).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already taken")

        user = models.User(username=username, email=email, hashed_password=self.hasher.hash(password))
        self.session.add(user)
        await self.session.flush([user])
        return user

    async def auth_user(self, username: str, password: str) -> models.User:
        clause = select(models.User).where(or_(col(models.User.username) == username, col(models.User.email) == username))
        user = (await self.session.exec(clause)).first()
        try:
            if not user:
                raise VerifyMismatchError("not found")
            self.hasher.verify(user.hashed_password, password)
            return user
        except VerifyMismatchError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    async def get_user(self, user_id: uuid.UUID) -> models.User | None:
        return await self.session.get(models.User, user_id)

    def generate_token(self, user: models.User) -> str:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=settings.jwt_expiration_days)
        payload = {"sub": str(user.id), "exp": int(expires_at.timestamp())}
        return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

    def verify_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

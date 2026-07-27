import uuid
from typing import Annotated

from argon2 import PasswordHasher
from fastapi import Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_perfectionist_starter.infra import engine, models


class UserService:
    def __init__(self, session: Annotated[AsyncSession, Depends(engine.get_db)]) -> None:
        self.session = session
        self.hasher = PasswordHasher()

    async def create_user(self, username: str, email: str, password: str) -> models.User:
        clause = select(models.User.id).where(or_(models.User.username == username, models.User.email == email))
        if (await self.session.execute(clause)).scalars().first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名或邮箱已被占用")

        user = models.User(username=username, email=email, hashed_password=self.hasher.hash(password))
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_user(self, user_id: uuid.UUID) -> models.User:
        user = await self.session.get(models.User, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
        return user

import uuid

from pydantic import EmailStr, Field

import fastapi_perfectionist_starter.infra.models as models


class UserResponse(models.BaseModel):
    id: uuid.UUID
    username: str
    email: str


class UserCreateRequest(models.BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=8)
    email: EmailStr

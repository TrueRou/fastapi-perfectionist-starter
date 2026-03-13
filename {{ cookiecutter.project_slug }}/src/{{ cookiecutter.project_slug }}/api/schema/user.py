import uuid
from datetime import datetime

from pydantic import EmailStr, Field

from {{ cookiecutter.project_slug }}.infra.models import BaseModel


class UserPublic(BaseModel):
    id: uuid.UUID
    username: str
    email: str


class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=8)
    email: EmailStr


class UserLoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class UserAuthResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int

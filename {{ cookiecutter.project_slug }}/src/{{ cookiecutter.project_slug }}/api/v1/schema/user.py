import uuid

from pydantic import EmailStr, Field

from {{ cookiecutter.project_slug }}.infra import models


class UserPublic(models.BaseModel):
    id: uuid.UUID
    username: str
    email: str


class UserCreateRequest(models.BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=8)
    email: EmailStr


class UserLoginRequest(models.BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class UserAuthResponse(models.BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int

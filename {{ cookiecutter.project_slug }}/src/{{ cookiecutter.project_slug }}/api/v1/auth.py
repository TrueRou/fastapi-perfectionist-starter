from typing import Annotated

from fastapi import APIRouter, Body, Depends, Form

from .schema.user import UserAuthResponse, UserCreateRequest, UserPublic
from {{ cookiecutter.project_slug }}.infra import models, response, settings
from {{ cookiecutter.project_slug }}.modules.user import RequireUser, UserService

router = APIRouter(tags=["auth"])


@router.post("/auth/register", response_model=response.AppResponse[UserPublic])
async def register(
    body: Annotated[UserCreateRequest, Body()],
    srv_user: Annotated[UserService, Depends()],
):
    user = await srv_user.create_user(body.username, body.email, body.password)
    return response.ResponseHandler.success(user)


@router.post("/auth/token", response_model=UserAuthResponse)
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    srv_user: Annotated[UserService, Depends()],
):
    user: models.User = await srv_user.auth_user(username, password)
    return UserAuthResponse(
        access_token=srv_user.generate_token(user),
        token_type="Bearer",
        expires_in=settings.jwt_expiration_days * 24 * 60 * 60,
    )


@router.get("/users/me", response_model=response.AppResponse[UserPublic])
async def get_current_user(
    dep_user: Annotated[models.User, Depends(RequireUser())],
):
    return response.ResponseHandler.success(dep_user)

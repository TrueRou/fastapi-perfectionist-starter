from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_perfectionist_starter.api.v1.schema.auth import AuthTokenResponse
from fastapi_perfectionist_starter.api.v1.schema.user import UserResponse
from fastapi_perfectionist_starter.infra import models, response
from fastapi_perfectionist_starter.infra.settings import settings
from fastapi_perfectionist_starter.modules.auth.dependencies import RequireAuthUser
from fastapi_perfectionist_starter.modules.auth.services import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=AuthTokenResponse)
async def get_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    srv_auth: Annotated[AuthService, Depends()],
) -> AuthTokenResponse:
    user: models.User = await srv_auth.get_user(form.username, form.password)
    return AuthTokenResponse(
        access_token=srv_auth.generate_token(user),
        token_type="Bearer",
        expires_in=settings.jwt_expiration_days * 24 * 60 * 60,
    )


@router.post("/me", response_model=response.AppResponse[UserResponse])
async def get_current_user(
    dep_user: Annotated[models.User, Depends(RequireAuthUser())],
) -> response.AppResponse[models.User]:
    return response.ResponseHandler.success(dep_user)

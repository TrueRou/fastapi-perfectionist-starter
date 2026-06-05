import uuid
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from {{ cookiecutter.project_slug }}.infra import models
from {{ cookiecutter.project_slug }}.modules.user import UserService

security_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token", auto_error=False)


class RequireUserOptional:
    async def __call__(
        self,
        dep_token: Annotated[str | None, Depends(security_scheme)],
        srv_user: Annotated[UserService, Depends()],
    ) -> models.User | None:
        if dep_token is None:
            return None

        payload = srv_user.verify_token(dep_token)
        try:
            user_id = uuid.UUID(payload.get("sub"))
        except TypeError, ValueError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed token")

        return await srv_user.get_user(user_id)


class RequireUser:
    async def __call__(
        self,
        dep_user: Annotated[models.User | None, Depends(RequireUserOptional())],
    ) -> Any:
        if dep_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
        return dep_user

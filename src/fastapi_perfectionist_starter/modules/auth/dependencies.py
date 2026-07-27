import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from fastapi_perfectionist_starter.infra import models
from fastapi_perfectionist_starter.modules.auth.services import AuthService
from fastapi_perfectionist_starter.modules.user.services import UserService

security_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/token", auto_error=False)


class RequireAuthUser:
    async def __call__(
        self,
        dep_token: Annotated[str, Depends(security_scheme)],
        srv_auth: Annotated[AuthService, Depends()],
        srv_user: Annotated[UserService, Depends()],
    ) -> models.User:
        payload = srv_auth.verify_token(dep_token)

        try:
            user_id = uuid.UUID(payload.get("sub"))
        except (TypeError, ValueError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="令牌格式无效") from None

        return await srv_user.get_user(user_id)

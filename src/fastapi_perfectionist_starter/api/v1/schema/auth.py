from fastapi_perfectionist_starter.infra import models


class AuthTokenResponse(models.BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int

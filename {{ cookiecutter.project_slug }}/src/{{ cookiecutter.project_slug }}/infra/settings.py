from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_host: str = Field(default="127.0.0.1")
    app_port: int = Field(default=8000, ge=1, le=65535)
    app_debug: bool = Field(default=False)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(default="INFO")

    database_url: str = Field(default="sqlite+aiosqlite:///./dev.db")

    jwt_secret: str = Field(default="change-this-in-production")
    jwt_expiration_days: int = Field(default=90)
    jwt_algorithm: str = Field(default="HS256")

    cors_origins: list[str] = Field(default=["http://localhost:3000", "http://localhost:5173"])

    @model_validator(mode="after")
    def validate_jwt_secret_in_production(self) -> "Settings":
        if not self.app_debug and self.jwt_secret == "change-this-in-production":
            raise ValueError(
                "jwt_secret must be changed from the default value when app_debug is False. "
                "Set JWT_SECRET in your environment or .env file."
            )
        return self


settings = Settings()

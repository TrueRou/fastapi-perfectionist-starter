from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_host: str = Field(default="127.0.0.1")
    app_port: int = Field(default=8000)
    app_debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")

    database_url: str = Field(default="sqlite+aiosqlite:///./dev.db")

    jwt_secret: str = Field(default="change-this-in-production")
    jwt_expiration_days: int = Field(default=90)


settings = Settings()

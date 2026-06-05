from datetime import datetime, timezone

from pydantic import BaseModel, Field


class AppResponse[T](BaseModel):
    data: T | None = None
    code: int = 200
    message: str = "success"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ResponseHandler:
    @staticmethod
    def success(data=None, message: str = "success") -> "AppResponse":
        return AppResponse(data=data, message=message)

    @staticmethod
    def error(message: str = "error", code: int = 500) -> "AppResponse[None]":
        return AppResponse(message=message, code=code)

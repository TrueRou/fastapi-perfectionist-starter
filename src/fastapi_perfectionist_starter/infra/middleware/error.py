from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from fastapi_perfectionist_starter.infra.logging import source
from fastapi_perfectionist_starter.infra.response import ResponseHandler

unexpected_error_response = ResponseHandler.error("服务器发生意外错误。").model_dump()


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.opt(exception=exc).patch(source()).exception(str(exc))
            return JSONResponse(status_code=500, content=unexpected_error_response)


def add_middleware(asgi_app: FastAPI) -> None:
    asgi_app.add_middleware(ExceptionHandlerMiddleware)


def add_exception_handler(asgi_app: FastAPI) -> None:
    @asgi_app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = exc.errors()
        if errors:
            error = errors[0]
            field = " -> ".join(str(loc) for loc in error.get("loc", []))
            msg = f"请求参数校验失败：{field} - {error.get('msg', '未知错误')}"
        else:
            msg = "请求参数校验失败"

        return JSONResponse(status_code=422, content=ResponseHandler.error(msg, 422).model_dump())

    @asgi_app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        logger.patch(source()).warning("{} {} ({})", request.method, request.url, str(exc.detail))
        return JSONResponse(
            status_code=exc.status_code,
            content=ResponseHandler.error(exc.detail, exc.status_code).model_dump(),
        )

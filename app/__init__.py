import json
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import ExceptionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.excpetions.RequestException import AuthException
from app.excpetions.RequestException import PermissionException

pity = FastAPI()


class PityException(Exception):
    def __init__(self, data: Any):
        if isinstance(data, bytes):
            self.data = data.decode()
        elif isinstance(data, dict):
            self.data = json.dumps(data, ensure_ascii=False)


class PartnerAvailabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        raise PityException(await request.body())
        return await call_next(request)


@pity.exception_handler(PityException)
async def custom_exception_handler(request: Request, exc: PityException):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "code": 110,
            "request_data": exc.data,
            "msg": "unknown error"
        })
    )


pity.add_middleware(PartnerAvailabilityMiddleware)
pity.add_middleware(ExceptionMiddleware, handlers=pity.exception_handlers)  # this is the change


def error_map(error_type: str, field: str):
    if "missing" in error_type:
        return f"缺少参数: {field}"
    if "params" in error_type:
        return f"参数: {field} 不规范"
    if "not_allowed" in error_type:
        return f"参数: {field} 类型不正确"


@pity.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "code": 101,
            "msg": error_map(exc.errors()[0]["type"], exc.errors()[0].get("loc", ['unknown'])[-1]) if len(
                exc.errors()) > 0 else "参数解析失败",
        })
    )


@pity.exception_handler(Exception)
async def unexpected_exception_error(request: Request, exc: Exception):
    await request.body()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "code": 110,
            "request_data": str(exc),
        })
    )


@pity.exception_handler(PermissionException)
async def unexpected_exception_error(request: Request, exc: PermissionException):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "code": 403,
            "msg": exc.detail,
        })
    )


@pity.exception_handler(AuthException)
async def unexpected_exception_error(request: Request, exc: AuthException):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "code": 401,
            "msg": exc.detail,
        })
    )

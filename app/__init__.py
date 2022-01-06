from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import ExceptionMiddleware
from starlette.types import Message

from app.excpetions.RequestException import AuthException
from app.excpetions.RequestException import PermissionException

pity = FastAPI()


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {"type": "http.request", "body": body}

    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.body()
    await set_body(request, body)
    return body


@pity.middleware("http")
async def errors_handling(request: Request, call_next):
    body = await request.body()
    try:
        await set_body(request, await request.body())
        return await call_next(request)
    except Exception as exc:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder({
                "code": 110,
                "msg": str(exc),
                "request_data": body,
            })
        )


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
            "msg": str(exc.detail),
        })
    )

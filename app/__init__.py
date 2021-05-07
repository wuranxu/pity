from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

pity = FastAPI()


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
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "code": 110,
            "msg": str(exc),
        })
    )


@pity.exception_handler(HTTPException)
async def unexpected_exception_error(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "code": 110,
            "msg": exc.detail,
        })
    )

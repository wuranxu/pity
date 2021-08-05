import json

from fastapi import Depends, APIRouter

from app.middleware.AsyncHttpClient import AsyncRequest
from app.routers import Permission
from app.routers.request.http_schema import HttpRequestForm
from app.utils.executor import Executor

router = APIRouter(prefix="/request")


@router.post("/http")
async def http_request(data: HttpRequestForm, user_info=Depends(Permission())):
    if "Content-Type" not in data.headers:
        data.headers['Content-Type'] = "application/json; charset=UTF-8"
    if "form" not in data.headers['Content-Type']:
        r = AsyncRequest(data.url, headers=data.headers,
                         data=data.body.encode() if data.body is not None else data.body)
    else:
        body = json.loads(data.body)
        r = AsyncRequest(data.url, headers=data.headers, data=body if body is not None else body)
    response = await r.invoke(data.method)
    if response.get("status"):
        return dict(code=0, data=response, msg="操作成功")
    return dict(code=110, data=response, msg=response.get("msg"))


@router.get("/run")
async def execute_case(case_id: int, user_info=Depends(Permission())):
    executor = Executor()
    result, err = await executor.run(case_id)
    if err:
        return dict(code=110, data=result, msg=err)
    return dict(code=0, data=result, msg="操作成功")

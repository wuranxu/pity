from fastapi import Depends, APIRouter

from app.middleware.HttpClient import Request
from app.routers import Permission
from app.routers.request.http_schema import HttpRequestForm
from app.utils.executor import Executor

router = APIRouter(prefix="/request")


@router.post("/http")
async def http_request(data: HttpRequestForm, user_info=Depends(Permission())):
    r = Request(data.url, data=data.body, headers=data.headers)
    response = r.request(data.method)
    if response.get("status"):
        return dict(code=0, data=response, msg="操作成功")
    return dict(code=110, data=response, msg=response.get("msg"))


@router.get("/run")
async def execute_case(case_id: int, user_info=Depends(Permission())):
    executor = Executor()
    result, err = executor.run(case_id)
    if err:
        return dict(code=110, data=result, msg=err)
    return dict(code=0, data=result, msg="操作成功")

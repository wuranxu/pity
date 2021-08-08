import asyncio
import json
from typing import List, Dict

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


@router.post("/run/async")
async def execute_case(case_id: List[int], user_info=Depends(Permission())):
    data = dict()
    # s = time.perf_counter()
    await asyncio.gather(*(run_single(c, data) for c in case_id))
    # elapsed = time.perf_counter() - s
    # print(f"async executed in {elapsed:0.2f} seconds.")
    return dict(code=0, data=data, msg="操作成功")


@router.post("/run/sync")
async def execute_case(case_id: List[int], user_info=Depends(Permission())):
    data = dict()
    # s = time.perf_counter()
    for c in case_id:
        executor = Executor()
        data[c] = await executor.run(c)
    # elapsed = time.perf_counter() - s
    # print(f"sync executed in {elapsed:0.2f} seconds.")
    return dict(code=0, data=data, msg="操作成功")


async def run_single(case_id: int, data: Dict[int, tuple]):
    executor = Executor()
    data[case_id] = await executor.run(case_id)

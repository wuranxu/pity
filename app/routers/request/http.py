import asyncio
import json
from typing import List, Dict

from fastapi import Depends, APIRouter

from app.dao.test_case.TestcaseDataDao import PityTestcaseDataDao
from app.handler.fatcory import PityResponse
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
async def execute_case(env: int, case_id: int, user_info=Depends(Permission())):
    try:
        executor = Executor()
        test_data = await PityTestcaseDataDao.list_testcase_data_by_env(env, case_id)
        ans = []
        for data in test_data:
            params = json.loads(data.json_data)
            result, err = await executor.run(env, case_id, request_param=params)
            if err:
                return PityResponse.failed(data=result, msg=err)
            ans.append(result)
        return PityResponse.success(ans)
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/run/async")
async def execute_case(env: int, case_id: List[int], user_info=Depends(Permission())):
    data = dict()
    # s = time.perf_counter()
    await asyncio.gather(*(run_single(env, c, data) for c in case_id))
    # elapsed = time.perf_counter() - s
    # print(f"async executed in {elapsed:0.2f} seconds.")
    return dict(code=0, data=data, msg="操作成功")


@router.post("/run/sync")
async def execute_case(env: int, case_id: List[int], user_info=Depends(Permission())):
    data = dict()
    # s = time.perf_counter()
    for c in case_id:
        executor = Executor()
        data[c] = await executor.run(env, c)
    # elapsed = time.perf_counter() - s
    # print(f"sync executed in {elapsed:0.2f} seconds.")
    return dict(code=0, data=data, msg="操作成功")


@router.post("/run/multiple")
async def execute_as_report(case_id: List[int], user_info=Depends(Permission())):
    report_id = await Executor.run_multiple(user_info['id'], 1, case_id)
    return dict(code=0, data=report_id, msg="操作成功")


async def run_single(env: int, case_id: int, data: Dict[int, tuple]):
    executor = Executor()
    data[case_id] = await executor.run(env, case_id)

import asyncio
import json
import uuid
from typing import List, Dict

from fastapi import Depends, APIRouter

from app.core.executor import Executor
from app.crud.test_case.TestcaseDataDao import PityTestcaseDataDao
from app.handler.fatcory import PityResponse
from app.middleware.AsyncHttpClient import AsyncRequest
from app.routers import Permission
from app.routers.request.http_schema import HttpRequestForm

router = APIRouter(prefix="/request")


@router.post("/http")
async def http_request(data: HttpRequestForm, user_info=Depends(Permission())):
    try:
        r = await AsyncRequest.client(data.url, data.body_type, headers=data.headers, body=data.body)
        response = await r.invoke(data.method)
        if response.get("status"):
            return PityResponse.success(response)
        return PityResponse.failed(response.get("msg"), data=response)
    except Exception as e:
        return PityResponse.failed(e)


@router.get("/run")
async def execute_case(env: int, case_id: int, user_info=Depends(Permission())):
    try:
        executor = Executor()
        test_data = await PityTestcaseDataDao.list_testcase_data_by_env(env, case_id)
        ans = dict()
        for data in test_data:
            params = json.loads(data.json_data)
            result, err = await executor.run(env, case_id, request_param=params)
            # if err:
            #     return PityResponse.failed(data=result, msg=err)
            ans[data.name] = result
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
    task_id = uuid.uuid5(uuid.NAMESPACE_URL, "task")

    # s = time.perf_counter()
    for c in case_id:
        executor = Executor()
        data[c] = await executor.run(env, c)
    # elapsed = time.perf_counter() - s
    # print(f"sync executed in {elapsed:0.2f} seconds.")
    return PityResponse.success(data)


@router.post("/run/multiple")
async def execute_as_report(env: int, case_id: List[int], user_info=Depends(Permission())):
    report_id = await Executor.run_multiple(user_info['id'], env, case_id)
    return PityResponse.success(report_id)


async def run_single(env: int, case_id: int, data: Dict[int, tuple]):
    executor = Executor()
    data[case_id] = await executor.run(env, case_id)

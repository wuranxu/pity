from fastapi import APIRouter, Depends

from app.dao.test_case.TestCaseAssertsDao import TestCaseAssertsDao
from app.dao.test_case.TestCaseDao import TestCaseDao
from app.handler.fatcory import ResponseFactory
from app.routers import Permission
from app.routers.testcase.testcase_schema import TestCaseForm, TestCaseAssertsForm

router = APIRouter(prefix="/testcase")


@router.post("/insert")
async def insert_testcase(data: TestCaseForm, user_info=Depends(Permission())):
    err = TestCaseDao.insert_test_case(data.dict(), user_info['id'])
    if err:
        return dict(code=110, msg=err)
    return dict(code=0, msg="操作成功")


@router.post("/update")
async def update_testcase(data: TestCaseForm, user_info=Depends(Permission())):
    err = TestCaseDao.update_test_case(data, user_info['id'])
    if err:
        return dict(code=110, msg=err)
    return dict(code=0, msg="操作成功")


@router.get("/query")
async def query_testcase(caseId: int, user_info=Depends(Permission())):
    data, err = TestCaseDao.query_test_case(caseId)
    if err:
        return dict(code=110, msg=err)
    return dict(code=0, data=ResponseFactory.model_to_dict(data), msg="操作成功")


@router.post("/asserts/insert")
def insert_testcase_asserts(data: TestCaseAssertsForm, user_info=Depends(Permission())):
    err = TestCaseAssertsDao.insert_test_case_asserts(**data.dict(), user=user_info["id"])
    if err:
        return dict(code=110, msg=err)
    return dict(code=0, msg="操作成功")

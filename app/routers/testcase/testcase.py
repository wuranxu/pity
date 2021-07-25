from fastapi import APIRouter, Depends

from app.dao.project.ProjectDao import ProjectDao
from app.dao.test_case.ConstructorDao import ConstructorDao
from app.dao.test_case.TestCaseAssertsDao import TestCaseAssertsDao
from app.dao.test_case.TestCaseDao import TestCaseDao
from app.handler.fatcory import ResponseFactory
from app.models.schema.constructor import ConstructorForm
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


@router.get("/list")
async def query_testcase(user_info=Depends(Permission())):
    try:
        projects, _, _ = ProjectDao.list_project(user_info["role"], user_info["id"], 1, 2000)
        data = TestCaseDao.list_testcase_tree(projects)
        return dict(code=0, data=data, msg="操作成功")
    except Exception as e:
        return dict(code=110, msg=str(e))


@router.post("/asserts/insert")
async def insert_testcase_asserts(data: TestCaseAssertsForm, user_info=Depends(Permission())):
    err = TestCaseAssertsDao.insert_test_case_asserts(**data.dict(), user=user_info["id"])
    if err:
        return dict(code=110, msg=err)
    return dict(code=0, msg="操作成功")


@router.post("/constructor/insert")
async def insert_constructor(data: ConstructorForm, user_info=Depends(Permission())):
    try:
        ConstructorDao.insert_constructor(data, user=user_info["id"])
        return dict(code=0, msg="操作成功")
    except Exception as e:
        return dict(code=110, msg=str(e))


@router.get("/constructor/tree")
async def get_constructor_tree(name: str = "", user_info=Depends(Permission())):
    try:
        result = ConstructorDao.get_constructor_tree(name)
        return dict(code=0, msg="操作成功", data=result)
    except Exception as e:
        return dict(code=110, msg=str(e))


@router.get("/constructor")
async def get_constructor_tree(id: int, user_info=Depends(Permission())):
    try:
        result = ConstructorDao.get_constructor_data(id)
        return dict(code=0, msg="操作成功", data=result)
    except Exception as e:
        return dict(code=110, msg=str(e))

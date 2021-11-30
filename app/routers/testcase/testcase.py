from typing import List

from fastapi import APIRouter, Depends

from app.dao.test_case.ConstructorDao import ConstructorDao
from app.dao.test_case.TestCaseAssertsDao import TestCaseAssertsDao
from app.dao.test_case.TestCaseDao import TestCaseDao
from app.dao.test_case.TestCaseDirectory import PityTestcaseDirectoryDao
from app.dao.test_case.TestReport import TestReportDao
from app.dao.test_case.TestcaseDataDao import PityTestcaseDataDao
from app.handler.fatcory import PityResponse
from app.models.schema.constructor import ConstructorForm, ConstructorIndex
from app.models.schema.testcase_data import PityTestcaseDataForm
from app.models.schema.testcase_directory import PityTestcaseDirectoryForm
from app.models.schema.testcase_schema import TestCaseAssertsForm, TestCaseForm
from app.routers import Permission

router = APIRouter(prefix="/testcase")


@router.get("/list")
async def list_testcase(directory_id: int = None, name: str = "", create_user: str = ''):
    try:
        data = await TestCaseDao.list_test_case(directory_id, name, create_user)
        return PityResponse.success(PityResponse.model_to_list(data))
    except Exception as e:
        return PityResponse.failed(str(e))


@router.post("/insert")
def insert_testcase(data: TestCaseForm, user_info=Depends(Permission())):
    try:
        case_id = TestCaseDao.insert_test_case(data.dict(), user_info['id'])
        return PityResponse.success(case_id)
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/update")
def update_testcase(data: TestCaseForm, user_info=Depends(Permission())):
    try:
        data = TestCaseDao.update_test_case(data, user_info['id'])
        return PityResponse.success(PityResponse.model_to_dict(data))
    except Exception as e:
        return PityResponse.failed(e)


@router.get("/query")
async def query_testcase(caseId: int, user_info=Depends(Permission())):
    try:
        data = await TestCaseDao.query_test_case(caseId)
        return PityResponse.success(PityResponse.dict_model_to_dict(data))
    except Exception as e:
        return PityResponse.failed(e)


# @router.get("/list")
# async def query_testcase(user_info=Depends(Permission())):
#     try:
#         projects, _, _ = ProjectDao.list_project(user_info["role"], user_info["id"], 1, 2000)
#         data = TestCaseDao.list_testcase_tree(projects)
#         return dict(code=0, data=data, msg="操作成功")
#     except Exception as e:
#         return dict(code=110, msg=str(e))


@router.post("/asserts/insert")
async def insert_testcase_asserts(data: TestCaseAssertsForm, user_info=Depends(Permission())):
    try:
        new_assert = await TestCaseAssertsDao.insert_test_case_asserts(data, user=user_info["id"])
        return PityResponse.success(PityResponse.model_to_dict(new_assert))
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/asserts/update")
async def insert_testcase_asserts(data: TestCaseAssertsForm, user_info=Depends(Permission())):
    try:
        updated = await TestCaseAssertsDao.update_test_case_asserts(data, user=user_info["id"])
        return PityResponse.success(PityResponse.model_to_dict(updated))
    except Exception as e:
        return PityResponse.failed(e)


@router.get("/asserts/delete")
async def insert_testcase_asserts(id: int, user_info=Depends(Permission())):
    try:
        await TestCaseAssertsDao.delete_test_case_asserts(id, user=user_info["id"])
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/constructor/insert")
async def insert_constructor(data: ConstructorForm, user_info=Depends(Permission())):
    try:
        await ConstructorDao.insert_constructor(data, user=user_info["id"])
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/constructor/update")
async def update_constructor(data: ConstructorForm, user_info=Depends(Permission())):
    try:
        await ConstructorDao.update_constructor(data, user=user_info["id"])
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(e)


@router.get("/constructor/delete")
async def update_constructor(id: int, user_info=Depends(Permission())):
    try:
        await ConstructorDao.delete_constructor(id, user=user_info["id"])
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/constructor/order")
def update_constructor_index(data: List[ConstructorIndex], user_info=Depends(Permission())):
    try:
        ConstructorDao.update_constructor_index(data)
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


# 获取数据构造器树
@router.get("/constructor")
async def get_constructor_tree(id: int, user_info=Depends(Permission())):
    try:
        result = ConstructorDao.get_constructor_data(id)
        return dict(code=0, msg="操作成功", data=result)
    except Exception as e:
        return dict(code=110, msg=str(e))


# 获取所有数据构造器
@router.get("/constructor/list")
async def list_case_and_constructor(constructor_type: int):
    try:
        ans = await ConstructorDao.get_case_and_constructor(constructor_type)
        return PityResponse.success(ans)
    except Exception as e:
        return PityResponse.failed(str(e))


# 根据id查询具体报告内容
@router.get("/report")
async def query_report(id: int, user_info=Depends(Permission())):
    try:
        report, case_list = await TestReportDao.query(id)
        return dict(code=0, data=dict(report=PityResponse.model_to_dict(report),
                                      case_list=PityResponse.model_to_list(case_list)), msg="操作成功")
    except Exception as e:
        return dict(code=110, msg=str(e))


# 获取构建历史记录
@router.get("/report/list")
async def list_report(page: int, size: int, start_time: str, end_time: str, executor: int = None,
                      user_info=Depends(Permission())):
    try:
        report_list, total = await TestReportDao.list_report(page, size, start_time, end_time, executor)
        return dict(code=0, data=PityResponse.model_to_list(report_list), msg="操作成功", total=total)
    except Exception as e:
        return dict(code=110, msg=str(e))


# 获取脑图数据
@router.get("/xmind")
async def get_xmind_data(case_id: int, user_info=Depends(Permission())):
    try:
        tree_data = await TestCaseDao.get_xmind_data(case_id)
        return PityResponse.success(tree_data)
    except Exception as e:
        return PityResponse.failed(e)


# 获取case目录
@router.get("/directory")
async def get_testcase_directory(project_id: int, user_info=Depends(Permission())):
    try:
        tree_data, _ = await PityTestcaseDirectoryDao.get_directory_tree(project_id)
        return PityResponse.success(tree_data)
    except Exception as e:
        return PityResponse.failed(e)


# 获取case目录+case
@router.get("/tree")
async def get_directory_and_case(project_id: int, user_info=Depends(Permission())):
    try:
        tree_data, cs_map = await PityTestcaseDirectoryDao.get_directory_tree(project_id,
                                                                              TestCaseDao.get_test_case_by_directory_id)
        return PityResponse.success(dict(tree=tree_data, case_map=cs_map))
    except Exception as e:
        return PityResponse.failed(e)


@router.get("/directory/query")
async def query_testcase_directory(directory_id: int, user_info=Depends(Permission())):
    try:
        data = await PityTestcaseDirectoryDao.query_directory(directory_id)
        return PityResponse.success(data)
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/directory/insert")
async def insert_testcase_directory(form: PityTestcaseDirectoryForm, user_info=Depends(Permission())):
    try:
        await PityTestcaseDirectoryDao.insert_directory(form, user_info['id'])
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/directory/update")
async def insert_testcase_directory(form: PityTestcaseDirectoryForm, user_info=Depends(Permission())):
    try:
        await PityTestcaseDirectoryDao.update_directory(form, user_info['id'])
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(e)


@router.get("/directory/delete")
async def insert_testcase_directory(id: int, user_info=Depends(Permission())):
    try:
        await PityTestcaseDirectoryDao.delete_directory(id, user_info['id'])
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/data/insert")
async def insert_testcase_data(form: PityTestcaseDataForm, user_info=Depends(Permission())):
    try:
        data = await PityTestcaseDataDao.insert_testcase_data(form, user_info['id'])
        return PityResponse.success(data)
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/data/update")
async def insert_testcase_data(form: PityTestcaseDataForm, user_info=Depends(Permission())):
    try:
        data = await PityTestcaseDataDao.update_testcase_data(form, user_info['id'])
        return PityResponse.success(data)
    except Exception as e:
        return PityResponse.failed(e)


@router.get("/data/delete")
async def insert_testcase_data(id: int, user_info=Depends(Permission())):
    try:
        await PityTestcaseDataDao.delete_testcase_data(id, user_info['id'])
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(e)

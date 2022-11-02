from app.crud.test_case.TestCaseAssertsDao import TestCaseAssertsDao
from app.crud.test_case.TestCaseDao import TestCaseDao
from app.crud.test_case.TestCaseOutParametersDao import PityTestCaseOutParametersDao
from app.crud.test_case.TestcaseDataDao import PityTestcaseDataDao
from app.models import async_session
from app.models.test_case import TestCase
from app.schema.testcase_schema import ListTestCaseForm, TestCaseForm, TestCaseInfo, DeleteTestCaseDto
from app.v1.service.testcase.proto.testcase_pb2_grpc import testcaseServicer
from app.v1.utils.context import Context, ctx


class TestCaseServiceApi(testcaseServicer):

    @ctx
    async def listTestCase(self, request, context):
        """获取测试用例数据
        :param request:
        :param context:
        :return:
        """
        form: ListTestCaseForm = Context.parse_args(request, ListTestCaseForm)
        data = await TestCaseDao.list_test_case(form.directory_id, form.name, form.create_user)
        return Context.success_json(data)

    @ctx
    async def insertTestCase(self, request, context):
        """添加测试用例
        :param request:
        :param context:
        :return:
        """
        user = Context.get_user(context)
        data: TestCaseForm = Context.parse_args(request, TestCaseForm)
        record = await TestCaseDao.query_record(name=data.name, directory_id=data.directory_id)
        if record is not None:
            return Context.failed("用例已存在")
        model = TestCase(**data.dict(), create_user=user.id)
        model = await TestCaseDao.insert(model=model, log=True)
        return Context.success_json(model.id)

    @ctx
    async def createTestCase(self, request, context):
        """创建测试用例，包含前后置条件和断言等数据
        :param request:
        :param context:
        :return:
        """
        user = Context.get_user(context)
        data: TestCaseInfo = Context.parse_args(request, TestCaseInfo)
        async with async_session() as session:
            async with session.begin():
                await TestCaseDao.insert_test_case(session, data, user.id)
        return Context.success()

    @ctx
    async def updateTestCase(self, request, context):
        """编辑测试用例
        :param request:
        :param context:
        :return:
        """
        form: TestCaseForm = Context.parse_args(request, TestCaseForm)
        user = Context.get_user(context)
        data = await TestCaseDao.update_test_case(form, user.id)
        result = await PityTestCaseOutParametersDao.update_many(form.id, form.out_parameters, user.id)
        return Context.success(dict(case_info=data, out_parameters=result))

    @ctx
    async def deleteTestCase(self, request, context):
        """删除测试用例
        :param request:
        :param context:
        :return:
        """
        form: DeleteTestCaseDto = Context.parse_args(request, TestCaseForm)
        user = Context.get_user(context)
        async with async_session() as session:
            async with session.begin():
                await TestCaseDao.delete_records(session, user.id, form.data)
                # 删除断言
                await TestCaseAssertsDao.delete_records(session, user.id, form.data, column="case_id")
                # 删除测试数据
                await PityTestcaseDataDao.delete_records(session, user.id, form.data, column="case_id")
                return Context.success()

    @ctx
    async def queryTestCase(self, request, context):
        """查询测试用例数据
        :param request:
        :param context:
        :return:
        """

from datetime import datetime, timedelta

from app.core.ws_connection_manager import ws_manage
from app.crud.project.ProjectDao import ProjectDao
from app.crud.statistics.dashboard import DashboardDao
from app.crud.test_case.TestCaseDao import TestCaseDao
from app.crud.test_case.TestPlan import PityTestPlanDao
from app.v1.service.dashboard.proto.dashboard_pb2_grpc import dashboardServicer
from app.v1.utils.context import Context, ctx


class DashboardServiceApi(dashboardServicer):

    @ctx
    async def queryTestPlanData(self, request, context):
        """查询测试计划统计信息
        :param request:
        :param context:
        :return:
        """
        user = Context.get_user(context)
        ans = await PityTestPlanDao.query_user_follow_test_plan(user.id)
        return Context.success_json(ans)

    @ctx
    async def statistics(self, request, context):
        """
        查询统计首页信息
        :param request:
        :param context:
        :return:
        """
        end = datetime.today()
        start = datetime.today() - timedelta(days=6)
        rank = await TestCaseDao.query_user_case_rank()
        count, data = await DashboardDao.get_statistics_data(start, end)
        report_data = await DashboardDao.get_report_statistics(start, end)
        online = ws_manage.get_clients()
        return Context.success_json(dict(count=count, data=data, rank=rank, clients=online, report=report_data))

    @ctx
    async def workspace(self, request, context):
        """
        获取用户工作台数据
        :param request:
        :param context:
        :return:
        """
        user = Context.get_user(context)
        count = await ProjectDao.query_user_project(user.id)
        rank = await TestCaseDao.query_user_case_list()
        now = datetime.now()
        weekly_case = await TestCaseDao.query_weekly_user_case(user.id, (now - timedelta(days=7)), now)
        case_count, user_rank = rank.get(str(user.id), [0, 0])
        return Context.success_json(dict(project_count=count, case_count=case_count,
                                         weekly_case=weekly_case,
                                         user_rank=user_rank, total_user=len(rank)))

from datetime import datetime, timedelta

from fastapi import Depends

from app.core.ws_connection_manager import ws_manage
from app.crud.statistics.dashboard import DashboardDao
from app.crud.test_case.TestCaseDao import TestCaseDao
from app.handler.fatcory import PityResponse
from app.routers import Permission
from app.routers.workspace.workspace import router


@router.get("/statistics", description="获取统计数据", summary="获取平台统计数据")
async def query_follow_testplan(_=Depends(Permission())):
    end = datetime.today()
    start = datetime.today() - timedelta(days=6)
    rank = await TestCaseDao.query_user_case_rank()
    count, data = await DashboardDao.get_statistics_data(start, end)
    report_data = await DashboardDao.get_report_statistics(start, end)
    online = ws_manage.get_clients()
    return PityResponse.success(dict(count=count, data=data, rank=rank, clients=online, report=report_data))

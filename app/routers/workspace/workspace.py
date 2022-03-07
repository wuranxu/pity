from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

from app.crud.project.ProjectDao import ProjectDao
from app.crud.test_case.TestCaseDao import TestCaseDao
from app.crud.test_case.TestPlan import PityTestPlanDao
from app.handler.fatcory import PityResponse
from app.routers import Permission

router = APIRouter(prefix="/workspace")


@router.get("/", description="获取工作台用户统计数据")
async def query_user_statistics(user_info=Depends(Permission())):
    user_id = user_info['id']
    count = await ProjectDao.query_user_project(user_id)
    rank = await TestCaseDao.query_user_case_list()
    now = datetime.now()
    weekly_case = await TestCaseDao.query_weekly_user_case(user_id, (now - timedelta(days=7)), now)
    case_count, user_rank = rank.get(str(user_id), [0, 0])
    return PityResponse.success(dict(project_count=count, case_count=case_count,
                                     weekly_case=weekly_case,
                                     user_rank=user_rank, total_user=len(rank)))


@router.get("/testplan", description="获取用户关注的测试计划执行数据")
async def query_follow_testplan(user_info=Depends(Permission())):
    user_id = user_info['id']
    ans = await PityTestPlanDao.query_user_follow_test_plan(user_id)
    return PityResponse.success(ans)

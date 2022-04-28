import asyncio

from apscheduler.jobstores.base import JobLookupError
from fastapi import Depends

from app.core.executor import Executor
from app.crud.test_case.TestPlan import PityTestPlanDao
from app.handler.fatcory import PityResponse
from app.schema.test_plan import PityTestPlanForm
from app.routers import Permission, get_session
from app.routers.testcase.testcase import router
from app.utils.scheduler import Scheduler
from config import Config


@router.get("/plan/list")
async def list_test_plan(page: int, size: int, project_id: int = None, name: str = "", priority: str = '',
                         create_user: int = None, follow: bool = None, user_info=Depends(Permission())):
    try:
        data, total = await PityTestPlanDao.list_test_plan(page, size, project_id=project_id, name=name,
                                                           follow=follow, priority=priority, role=user_info['role'],
                                                           create_user=create_user, user_id=user_info['id'])

        ans = Scheduler.list_test_plan(data)
        return PityResponse.success_with_size(ans, total=total)
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/plan/insert")
async def insert_test_plan(form: PityTestPlanForm, user_info=Depends(Permission(Config.MANAGER))):
    try:
        plan = await PityTestPlanDao.insert_test_plan(form, user_info['id'])
        # 添加定时任务
        Scheduler.add_test_plan(plan.id, plan.name, plan.cron)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(str(e))


@router.post("/plan/update")
async def update_test_plan(form: PityTestPlanForm, user_info=Depends(Permission(Config.MANAGER))):
    try:
        await PityTestPlanDao.update_test_plan(form, user_info['id'], True)
        Scheduler.edit_test_plan(form.id, form.name, form.cron)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(str(e))


@router.get("/plan/delete")
async def delete_test_plan(id: int, user_info=Depends(Permission(Config.MANAGER)), session=Depends(get_session)):
    try:
        await PityTestPlanDao.delete_record_by_id(session, user_info['id'], id)
        Scheduler.remove(id)
    except JobLookupError:
        # 说明没找到job
        pass
    except Exception as e:
        return PityResponse.failed(str(e))
    return PityResponse.success()


@router.get("/plan/switch")
async def switch_test_plan(id: int, status: bool, user_info=Depends(Permission(Config.MANAGER))):
    try:
        Scheduler.pause_resume_test_plan(id, status)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(str(e))


@router.get("/plan/execute")
async def run_test_plan(id: int, user_info=Depends(Permission(Config.MEMBER))):
    try:
        asyncio.create_task(Executor.run_test_plan(id, user_info['id']))
        return PityResponse.success("开始执行，请耐心等待")
    except Exception as e:
        return PityResponse.failed(str(e))


@router.get("/plan/follow", description="关注测试计划")
async def follow_test_plan(id: int, user_info=Depends(Permission(Config.MEMBER))):
    try:
        await PityTestPlanDao.follow_test_plan(id, user_info['id'])
        return PityResponse.success(msg="关注成功")
    except Exception as e:
        return PityResponse.failed(str(e))


@router.get("/plan/unfollow", description="取消关注测试计划")
async def unfollow_test_plan(id: int, user_info=Depends(Permission(Config.MEMBER))):
    try:
        await PityTestPlanDao.unfollow_test_plan(id, user_info['id'])
        return PityResponse.success(msg="取关成功")
    except Exception as e:
        return PityResponse.failed(str(e))

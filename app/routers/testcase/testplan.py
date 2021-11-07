from fastapi import Depends

from app.dao.test_case.TestPlan import PityTestPlanDao
from app.handler.fatcory import PityResponse
from app.models.schema.test_plan import PityTestPlanForm
from app.routers import Permission
from app.routers.testcase.testcase import router
from app.utils.scheduler import Scheduler
from config import Config


@router.get("/plan/list")
async def list_test_plan(page: int, size: int, project_id: int = None, name: str = "", priority: str = '',
                         create_user: int = None, user_info=Depends(Permission())):
    try:
        data, total = await PityTestPlanDao.list_test_plan(page, size, project_id, name, priority, create_user)
        ans = PityResponse.model_to_list(data)
        Scheduler.list_test_plan(ans)
        return PityResponse.success_with_size(ans, total=total)
    except Exception as e:
        return PityResponse.failed(str(e))


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
        await PityTestPlanDao.update_test_plan(form, user_info['id'])
        Scheduler.edit_test_plan(form.id, form.name, form.cron)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(str(e))


@router.get("/plan/delete")
async def delete_test_plan(id: int, user_info=Depends(Permission(Config.MANAGER))):
    try:
        await PityTestPlanDao.delete_test_plan(id, user_info['id'])
        Scheduler.remove(id)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(str(e))


@router.get("/plan/switch")
async def switch_test_plan(id: int, status: bool, user_info=Depends(Permission(Config.MANAGER))):
    try:
        Scheduler.pause_resume_test_plan(id, status)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(str(e))

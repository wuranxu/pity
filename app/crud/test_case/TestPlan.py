import asyncio
from copy import deepcopy

from sqlalchemy import select

from app.crud import Mapper
from app.models import async_session, DatabaseHelper
from app.models.schema.test_plan import PityTestPlanForm
from app.models.test_plan import PityTestPlan
from app.utils.decorator import dao
from app.utils.logger import Log
from config import Config


@dao(PityTestPlan, Log("PityTestPlanDao"))
class PityTestPlanDao(Mapper):

    @staticmethod
    async def list_test_plan(page: int, size: int, project_id: int = None, name: str = '', priority: str = '',
                             create_user: int = None):
        try:
            async with async_session() as session:
                conditions = [PityTestPlan.deleted_at == 0]
                DatabaseHelper.where(project_id, PityTestPlan.project_id == project_id, conditions) \
                    .where(name, PityTestPlan.name.like(f"%{name}%"), conditions) \
                    .where(priority, PityTestPlan.priority == priority, conditions) \
                    .where(create_user, PityTestPlan.create_user == create_user, conditions)
                sql = select(PityTestPlan).where(*conditions)
                result, total = await DatabaseHelper.pagination(page, size, session, sql)
                return result, total
        except Exception as e:
            PityTestPlanDao.log.error(f"获取测试计划失败: {str(e)}")
            raise Exception(f"获取测试计划失败: {str(e)}")

    @staticmethod
    async def insert_test_plan(plan: PityTestPlanForm, user: int) -> PityTestPlan:
        try:
            async with async_session() as session:
                async with session.begin():
                    query = await session.execute(select(PityTestPlan).where(PityTestPlan.project_id == plan.project_id,
                                                                             PityTestPlan.name == plan.name,
                                                                             PityTestPlan.deleted_at == 0))
                    if query.scalars().first() is not None:
                        raise Exception("测试计划已存在")
                    test_plan = PityTestPlan(**plan.dict(), user=user)
                    session.add(test_plan)
                    await session.flush()
                    await session.refresh(test_plan)
                    session.expunge(test_plan)
                    return test_plan
        except Exception as e:
            PityTestPlanDao.log.error(f"新增测试计划失败: {str(e)}")
            raise Exception(f"添加失败: {str(e)}")

    @classmethod
    async def update_test_plan(cls, plan: PityTestPlanForm, user: int, log=False):
        try:
            async with async_session() as session:
                async with session.begin():
                    query = await session.execute(
                        select(PityTestPlan).where(PityTestPlan.id == plan.id, PityTestPlan.deleted_at == 0))
                    data = query.scalars().first()
                    if data is None:
                        raise Exception("测试计划不存在")
                    old = deepcopy(data)
                    plan.env = ",".join(map(str, plan.env))
                    plan.receiver = ",".join(map(str, plan.receiver))
                    plan.case_list = ",".join(map(str, plan.case_list))
                    plan.msg_type = ",".join(map(str, plan.msg_type))
                    changed = DatabaseHelper.update_model(data, plan, user)
                    await session.flush()
                    session.expunge(data)
                if log:
                    async with session.begin():
                        await asyncio.create_task(cls.insert_log(session, user, Config.OperationType.UPDATE, data, old, plan.id, changed))
        except Exception as e:
            PityTestPlanDao.log.error(f"编辑测试计划失败: {str(e)}")
            raise Exception(f"编辑失败: {str(e)}")

    @staticmethod
    async def update_test_plan_state(id: int, state: int):
        try:
            async with async_session() as session:
                async with session.begin():
                    query = await session.execute(
                        select(PityTestPlan).where(PityTestPlan.id == id, PityTestPlan.deleted_at == 0))
                    data = query.scalars().first()
                    if data is None:
                        raise Exception("测试计划不存在")
                    data.state = state
        except Exception as e:
            PityTestPlanDao.log.error(f"编辑测试计划失败: {str(e)}")
            raise Exception(f"编辑失败: {str(e)}")

    @staticmethod
    async def query_test_plan(id: int) -> PityTestPlan:
        try:
            async with async_session() as session:
                sql = select(PityTestPlan).where(PityTestPlan.deleted_at == 0, PityTestPlan.id == id)
                data = await session.execute(sql)
                return data.scalars().first()
        except Exception as e:
            PityTestPlanDao.log.error(f"获取测试计划失败: {str(e)}")
            raise Exception(f"获取测试计划失败: {str(e)}")

    # @staticmethod
    # async def delete_test_plan(id: int, user: int):
    #     try:
    #         async with async_session() as session:
    #             async with session.begin():
    #                 query = await session.execute(
    #                     select(PityTestPlan).where(PityTestPlan.id == id, PityTestPlan.deleted_at == 0))
    #                 data = query.scalars().first()
    #                 if data is None:
    #                     raise Exception("测试计划不存在")
    #                 DatabaseHelper.delete_model(data, user)
    #     except Exception as e:
    #         PityTestPlanDao.log.error(f"删除测试计划失败: {str(e)}")
    #         raise Exception(f"删除失败: {str(e)}")

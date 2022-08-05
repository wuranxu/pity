from collections import defaultdict
from typing import List

from sqlalchemy import select

from app.crud import Mapper, ModelWrapper
from app.models import async_session, DatabaseHelper
from app.models.testcase_data import PityTestcaseData
from app.schema.testcase_data import PityTestcaseDataForm


@ModelWrapper(PityTestcaseData)
class PityTestcaseDataDao(Mapper):

    @classmethod
    async def insert_testcase_data(cls, form: PityTestcaseDataForm, user_id: int):
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(PityTestcaseData).where(PityTestcaseData.case_id == form.case_id,
                                                         PityTestcaseData.env == form.env,
                                                         PityTestcaseData.name == form.name,
                                                         PityTestcaseData.deleted_at == 0)
                    result = await session.execute(sql)
                    query = result.scalars().first()
                    if query is not None:
                        raise Exception("该数据已存在, 请重新编辑")
                    data = PityTestcaseData(**form.dict(), user_id=user_id)
                    session.add(data)
                    await session.flush()
                    await session.refresh(data)
                    session.expunge(data)
                    return data
        except Exception as e:
            cls.__log__.error(f"新增测试数据失败, error: {str(e)}")
            raise Exception(f"新增测试数据失败, {str(e)}")

    @classmethod
    async def update_testcase_data(cls, form: PityTestcaseDataForm, user: int):
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(PityTestcaseData).where(PityTestcaseData.id == form.id,
                                                         PityTestcaseData.deleted_at == 0)
                    result = await session.execute(sql)
                    query = result.scalars().first()
                    if query is None:
                        raise Exception("测试数据不存在")
                    cls.update_model(query, form, user)
                    await session.flush()
                    session.expunge(query)
                    return query
        except Exception as e:
            cls.__log__.error(f"编辑测试数据失败, error: {str(e)}")
            raise Exception(f"编辑测试数据失败, {str(e)}")

    @classmethod
    async def delete_testcase_data(cls, id: int, user: int):
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(PityTestcaseData).where(PityTestcaseData.id == id,
                                                         PityTestcaseData.deleted_at == 0)
                    result = await session.execute(sql)
                    query = result.scalars().first()
                    if query is None:
                        raise Exception("测试数据不存在")
                    cls.delete_model(query, user)
        except Exception as e:
            cls.__log__.error(f"删除测试数据失败, error: {str(e)}")
            raise Exception(f"删除测试数据失败, {str(e)}")

    @classmethod
    async def list_testcase_data(cls, case_id: int):
        ans = defaultdict(list)
        try:
            async with async_session() as session:
                sql = select(PityTestcaseData).where(PityTestcaseData.case_id == case_id,
                                                     PityTestcaseData.deleted_at == 0)
                result = await session.execute(sql)
                query = result.scalars().all()
                for q in query:
                    ans[q.env].append(q)
                return ans
        except Exception as e:
            cls.__log__.error(f"查询测试数据失败, error: {str(e)}")
            raise Exception(f"查询测试数据失败, {str(e)}")

    @classmethod
    async def list_testcase_data_by_env(cls, env: int, case_id: int) -> List[PityTestcaseData]:
        try:
            async with async_session() as session:
                sql = select(PityTestcaseData).where(PityTestcaseData.case_id == case_id,
                                                     PityTestcaseData.env == env,
                                                     PityTestcaseData.deleted_at == 0)
                result = await session.execute(sql)
                return result.scalars().all()
        except Exception as e:
            cls.__log__.error(f"查询测试数据失败, error: {str(e)}")
            raise Exception(f"查询测试数据失败, {str(e)}")

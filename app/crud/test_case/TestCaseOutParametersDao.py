import time
from datetime import datetime
from typing import List

from sqlalchemy import select, update

from app.crud import Mapper, ModelWrapper
from app.middleware.RedisManager import RedisHelper
from app.models import async_session
from app.models.out_parameters import PityTestCaseOutParameters
from app.schema.testcase_out_parameters import PityTestCaseOutParametersForm


@ModelWrapper(PityTestCaseOutParameters)
class PityTestCaseOutParametersDao(Mapper):

    @classmethod
    async def should_remove(cls, before, after):
        """
        找出要删除的数据
        :param before:
        :param after:
        :return:
        """
        data = []
        for b in before:
            for a in after:
                if a.id == b.id:
                    break
            else:
                data.append(b.id)
        return data

    @classmethod
    @RedisHelper.up_cache("dao")
    async def update_many(cls, case_id: int, data: List[PityTestCaseOutParametersForm], user_id: int):
        result = []
        try:
            async with async_session() as session:
                async with session.begin():
                    source = await session.execute(select(PityTestCaseOutParameters).where(
                        PityTestCaseOutParameters.case_id == case_id,
                        PityTestCaseOutParameters.deleted_at == 0,
                    ))
                    before = source.scalars().all()
                    should_remove = await cls.should_remove(before, data)
                    for item in data:
                        if item.id is None:
                            # add
                            temp = PityTestCaseOutParameters(**item.dict(), case_id=case_id, user_id=user_id)
                            session.add(temp)
                        else:
                            query = await session.execute(select(PityTestCaseOutParameters).where(
                                PityTestCaseOutParameters.id == item.id,
                            ))
                            temp = query.scalars().first()
                            if temp is None:
                                # 走新增逻辑
                                temp = PityTestCaseOutParameters(**item.dict(), case_id=case_id, user_id=user_id)
                                session.add(temp)
                            else:
                                temp.name = item.name
                                # temp.case_id = case_id
                                temp.expression = item.expression
                                temp.source = item.source
                                temp.match_index = item.match_index
                                temp.update_user = user_id
                                temp.updated_at = datetime.now()
                        await session.flush()
                        session.expunge(temp)
                        result.append(temp)
                    if should_remove:
                        await session.execute(
                            update(PityTestCaseOutParameters).where(
                                PityTestCaseOutParameters.id.in_(should_remove)).values(
                                deleted_at=int(time.time() * 1000)))
            return result
        except Exception as e:
            cls.__log__.error(f"批量更新出参数据失败: {e}")
            raise Exception(f"批量更新出参数据失败: {e}")

from datetime import datetime

from sqlalchemy import func, select

from app.crud import Mapper, ModelWrapper
from app.models import async_session
from app.models.operation_log import PityOperationLog


@ModelWrapper(PityOperationLog)
class PityOperationDao(Mapper):

    @classmethod
    async def count_user_activities(cls, user_id, start_time: datetime, end_time: datetime):
        """
        根据开始/结束时间 获取用户的活动日历（操作记录的数量）
        :param user_id:
        :param start_time:
        :param end_time:
        :return:
        """
        async with async_session() as session:
            async with session.begin():
                sql = select(PityOperationLog.operate_time, func.count(PityOperationLog.id)).where(
                    PityOperationLog.operate_time.between(start_time, end_time),
                    PityOperationLog.user_id == user_id) \
                    .group_by(PityOperationLog.operate_time).order_by(PityOperationLog.operate_time)
                data = await session.execute(sql)
                return data.all()

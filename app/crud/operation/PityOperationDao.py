from sqlalchemy import func, select

from app.crud import Mapper
from app.models import async_session
from app.models.operation_log import PityOperationLog
from app.utils.decorator import dao
from app.utils.logger import Log


@dao(PityOperationLog, Log("PityOperationDao"))
class PityOperationDao(Mapper):

    @classmethod
    async def count_user_activities(cls, user_id, start_time: str, end_time: str):
        """
        根据开始/结束时间 获取用户的活动日历（操作记录的数量）
        :param user_id:
        :param start_time:
        :param end_time:
        :return:
        """
        async with async_session() as session:
            async with session.begin():
                format_date = func.date_format(PityOperationLog.operate_time, "%Y-%m-%d")
                sql = select(format_date, func.count(PityOperationLog.id)).where(
                    PityOperationLog.operate_time.between(start_time, end_time),
                    PityOperationLog.user_id == user_id) \
                    .group_by(format_date).order_by(format_date)
                data = await session.execute(sql)
                return data.all()

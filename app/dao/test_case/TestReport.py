from datetime import datetime

from sqlalchemy import select

from app.models import async_session
from app.models.report import PityReport
from app.utils.logger import Log


class TestReportDao(object):
    log = Log("TestReportDao")

    @staticmethod
    async def start(executor: int, env: int, mode: int = 0) -> int:
        """
        生成buildId，开始执行任务，任务完成后通过回调方法更新报告
        :return: 返回report_id
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    report = PityReport(executor, env, mode=mode)
                    session.add(report)
                    await session.flush()
                    return report.id
        except Exception as e:
            TestReportDao.log.error(f"新增报告失败, error: {e}")
            raise Exception("新增报告失败")

    @staticmethod
    async def end(report_id: int, success_count: int, failed_count: int,
                  error_count: int, skipped_count: int, status: int) -> None:
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(PityReport).where(PityReport.id == report_id)
                    data = await session.execute(sql)
                    report = data.scalars().first()
                    if report is None:
                        raise Exception("获取报告失败")
                    report.status = status
                    report.success_count = success_count
                    report.failed_count = failed_count
                    report.error_count = error_count
                    report.skipped_count = skipped_count
                    report.finished_at = datetime.now()
                    await session.flush()
        except Exception as e:
            TestReportDao.log.error(f"更新报告失败, error: {e}")
            raise Exception("更新报告失败")

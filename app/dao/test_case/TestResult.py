from datetime import datetime

from app.models import async_session
from app.models.result import PityTestResult
from app.utils.logger import Log


class TestResultDao(object):
    log = Log("TestResultDao")

    @staticmethod
    async def insert(report_id: int, case_id: int, status: int,
                     case_log: str, start_at: datetime, finished_at: datetime,
                     url: str, body: str, request_method: str, cost: str,
                     asserts: str, response_headers: str, response: str,
                     status_code: int, cookies: str, retry: int = None, ) -> None:
        try:
            async with async_session() as session:
                async with session.begin():
                    report = PityTestResult(report_id, case_id, status,
                                            case_log, start_at, finished_at,
                                            url, body, request_method, cost,
                                            asserts, response_headers, response,
                                            status_code, cookies, retry)
                    session.add(report)
                    await session.flush()
        except Exception as e:
            TestResultDao.log.error(f"新增测试结果失败, error: {e}")
            raise Exception("新增测试结果失败")

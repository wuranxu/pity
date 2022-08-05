from datetime import datetime
from typing import List

from sqlalchemy import asc
from sqlalchemy.future import select

from app.crud import Mapper
from app.models import async_session
from app.models.result import PityTestResult
from app.models.test_case import TestCase
from app.utils.logger import Log


class TestResultDao(Mapper):
    log = Log("TestResultDao")

    @staticmethod
    async def insert_report(report_id: int, case_id: int, case_name: str, status: int,
                     case_log: str, start_at: datetime, finished_at: datetime,
                     url: str, body: str, request_method: str, request_headers: str, cost: str,
                     asserts: str, response_headers: str, response: str,
                     status_code: int, cookies: str, retry: int = None,
                     request_params: str = '', data_name: str = '', data_id: int = None,
                     ) -> None:
        try:
            async with async_session() as session:
                async with session.begin():
                    result = PityTestResult(report_id, case_id, case_name, status,
                                            case_log, start_at, finished_at,
                                            url, body, request_method, request_headers, cost,
                                            asserts, response_headers, response, status_code,
                                            cookies, retry, request_params, data_name, data_id)
                    session.add(result)
                    await session.flush()
        except Exception as e:
            TestResultDao.log.error(f"新增测试结果失败, error: {e}")
            raise Exception("新增测试结果失败")

    @staticmethod
    async def list(report_id: int) -> List[PityTestResult]:
        try:
            async with async_session() as session:
                sql = select(PityTestResult, TestCase.directory_id).join(TestCase,
                                                                         TestCase.id == PityTestResult.case_id). \
                    where(PityTestResult.report_id == report_id,
                          PityTestResult.deleted_at == 0).order_by(
                    asc(PityTestResult.case_id), asc(PityTestResult.start_at))
                data = await session.execute(sql)
                ans = []
                for res, directory_id in data.all():
                    res.directory_id = directory_id
                    ans.append(res)
                return ans
        except Exception as e:
            TestResultDao.log.error(f"获取测试用例执行记录失败, error: {e}")
            raise Exception("获取测试用例执行记录失败")

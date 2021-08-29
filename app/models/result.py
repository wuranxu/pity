from datetime import datetime

from sqlalchemy import INT, Column, DATETIME, String
from sqlalchemy import SMALLINT
from sqlalchemy import TEXT
from sqlalchemy.dialects.mysql import LONGTEXT

from app.models import Base


class PityTestResult(Base):
    __tablename__ = 'pity_test_result'
    id = Column(INT, primary_key=True)

    # 报告id
    report_id = Column(INT, index=True)

    # case_id
    case_id = Column(INT, index=True)

    # case_name
    case_name = Column(String(32))

    status = Column(SMALLINT, comment="对应状态 0: 成功 1: 失败 2: 出错 3: 跳过")

    # 开始时间
    start_at = Column(DATETIME, nullable=False)
    # 结束时间
    finished_at = Column(DATETIME, nullable=False)

    case_log = Column(TEXT)

    # 重试次数，预留字段
    retry = Column(INT, default=0)

    # http状态码
    status_code = Column(INT)

    url = Column(TEXT, nullable=False)

    body = Column(TEXT)

    request_method = Column(String(12), nullable=True)

    request_headers = Column(TEXT)

    cost = Column(String(12), nullable=False)

    asserts = Column(TEXT)

    response_headers = Column(TEXT)

    response = Column(LONGTEXT)

    cookies = Column(TEXT)

    deleted_at = Column(DATETIME, index=True)

    def __init__(self, report_id: int, case_id: int, case_name: str, status: int,
                 case_log: str, start_at: datetime, finished_at: datetime,
                 url: str, body: str, request_method: str, request_headers: str, cost: str,
                 asserts: str, response_headers: str, response: str,
                 status_code: int, cookies: str, retry: int = None,
                 ):
        self.report_id = report_id
        self.case_id = case_id
        self.case_name = case_name
        self.status = status
        self.case_log = case_log
        self.start_at = start_at
        self.finished_at = finished_at
        self.status = status
        self.retry = retry
        self.status_code = status_code
        self.url = url
        self.request_method = request_method
        self.request_headers = request_headers
        self.body = body
        self.cost = cost
        self.response = response
        self.response_headers = response_headers
        self.asserts = asserts
        self.cookies = cookies
        self.deleted_at = None

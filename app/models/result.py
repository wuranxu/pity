from datetime import datetime

from sqlalchemy import INT, Column, TIMESTAMP, String, BIGINT
from sqlalchemy import SMALLINT
from sqlalchemy import TEXT

from app.models import Base


class PityTestResult(Base):
    __tablename__ = 'pity_test_result'
    id = Column(INT, primary_key=True)

    directory_id = None

    # 报告id
    report_id = Column(INT, index=True)

    # case_id
    case_id = Column(INT, index=True)

    # case_name
    case_name = Column(String(32))

    status = Column(SMALLINT, comment="对应状态 0: 成功 1: 失败 2: 出错 3: 跳过")

    # 开始时间
    start_at = Column(TIMESTAMP, nullable=False)
    # 结束时间
    finished_at = Column(TIMESTAMP, nullable=False)

    case_log = Column(TEXT)

    # 重试次数，预留字段
    retry = Column(INT, default=0)

    # http状态码
    status_code = Column(INT)

    url = Column(TEXT)

    body = Column(TEXT)

    request_params = Column(TEXT)

    data_name = Column(String(24))

    data_id = Column(INT)

    request_method = Column(String(12), nullable=True)

    request_headers = Column(TEXT)

    cost = Column(String(12), nullable=False)

    asserts = Column(TEXT)

    response_headers = Column(TEXT)

    response = Column(TEXT)

    cookies = Column(TEXT)

    deleted_at = Column(BIGINT, nullable=False, default=0)

    def __init__(self, report_id: int, case_id: int, case_name: str, status: int,
                 case_log: str, start_at: datetime, finished_at: datetime,
                 url: str, body: str, request_method: str, request_headers: str, cost: str,
                 asserts: str, response_headers: str, response: str,
                 status_code: int, cookies: str, retry: int = None,
                 request_params: str = '', data_name: str = '', data_id: int = None
                 ):
        self.report_id = report_id
        self.case_id = case_id
        self.case_name = case_name
        self.status = status
        self.case_log = case_log
        self.start_at = start_at
        self.finished_at = finished_at
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
        self.request_params = request_params
        self.data_name = data_name
        self.data_id = data_id
        self.deleted_at = 0

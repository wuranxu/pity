from typing import List

from sqlalchemy import Column, String, INT, TEXT, SMALLINT, UniqueConstraint

from app.models.basic import PityBase
from app.models.out_parameters import PityTestCaseOutParameters


class TestCase(PityBase):
    __tablename__ = "pity_testcase"
    name = Column(String(32), index=True)
    request_type = Column(INT, default=1, comment="请求类型 1: http 2: grpc 3: dubbo")
    url = Column(TEXT, nullable=False, comment="请求url")
    request_method = Column(String(12), nullable=True, comment="请求方式, 如果非http可为空")
    request_headers = Column(TEXT, comment="请求头，可为空")
    # params = Column(TEXT, comment="请求params")
    # 2022-04-05 add base_path
    base_path = Column(String(24), comment="请求base_path")
    body = Column(TEXT, comment="请求body")
    body_type = Column(INT, comment="请求类型, 0: none 1: json 2: form 3: x-form 4: binary 5: GraphQL")
    directory_id = Column(INT, comment="所属目录")
    tag = Column(String(64), comment="用例标签")
    status = Column(INT, comment="用例状态: 1: 调试中 2: 暂时关闭 3: 正常运作")
    priority = Column(String(3), comment="用例优先级: P0-P4")
    # catalogue = Column(String(12), comment="用例目录")
    # expected = Column(TEXT, comment="预期结果, 支持el表达式", nullable=False)
    case_type = Column(SMALLINT, comment="0: 普通用例 1: 前置用例 2: 数据工厂")
    out_parameters: List[PityTestCaseOutParameters] = None
    # 调整联合唯一索引
    __table_args__ = (
        UniqueConstraint('directory_id', 'name', 'deleted_at'),
    )
    __tag__ = "测试用例"
    __fields__ = (name, request_type, url, request_method,
                  request_headers, body, body_type, directory_id,
                  tag, status, priority, case_type)
    __alias__ = dict(name="名称", request_type="请求协议", url="地址", request_method="请求方式",
                     request_headers="请求头", body="请求体", body_type="请求类型",
                     directory_id="用例目录", tag="标签", status="状态", priority="优先级",
                     case_type="用例类型")

    def __init__(self, name, request_type, url, directory_id, status, priority, create_user,
                 body_type=1, base_path=None, out_parameters=None,
                 tag=None, request_headers=None, case_type=0, body=None, request_method=None, id=None):
        super().__init__(create_user, id)
        self.name = name
        self.request_type = request_type
        self.url = url
        self.priority = priority
        self.directory_id = directory_id
        self.tag = tag
        # self.catalogue = catalogue
        self.status = status
        # self.expected = expected
        self.out_parameters = out_parameters
        self.body_type = body_type
        self.case_type = case_type
        self.body = body
        self.request_headers = request_headers
        self.request_method = request_method
        self.base_path = base_path

    def __str__(self):
        return f"[用例: {self.name}]({self.id})"

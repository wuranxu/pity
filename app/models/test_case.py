from datetime import datetime

from sqlalchemy import Column, String, INT, TEXT, DATETIME

from app.models import Base


class TestCase(Base):
    __tablename__ = "pity_testcase"
    id = Column(INT, primary_key=True)
    name = Column(String(32), unique=True, index=True)
    request_type = Column(INT, default=1, comment="请求类型 1: http 2: grpc 3: dubbo")
    url = Column(TEXT, nullable=False, comment="请求url")
    request_method = Column(String(12), nullable=True, comment="请求方式, 如果非http可为空")
    request_header = Column(TEXT, comment="请求头，可为空")
    # params = Column(TEXT, comment="请求params")
    body = Column(TEXT, comment="请求body")
    project_id = Column(INT, comment="所属项目")
    tag = Column(String(64), comment="用例标签")
    status = Column(INT, comment="用例状态: 1: 调试中 2: 暂时关闭 3: 正常运作")
    priority = Column(String(3), comment="用例优先级: p0-p3")
    catalogue = Column(String(12), comment="用例目录")
    # expected = Column(TEXT, comment="预期结果, 支持el表达式", nullable=False)
    created_at = Column(DATETIME, nullable=False)
    updated_at = Column(DATETIME, nullable=False)
    deleted_at = Column(DATETIME)
    create_user = Column(INT, nullable=False)
    update_user = Column(INT, nullable=False)

    def __init__(self, name, request_type, url, project_id, status, priority, create_user,
                 catalogue, tag=None, request_header=None, body=None, request_method=None, id=0):
        self.id = id
        self.name = name
        self.request_type = request_type
        self.url = url
        self.priority = priority
        self.project_id = project_id
        self.tag = tag
        self.catalogue = catalogue
        self.status = status
        # self.expected = expected
        self.body = body
        self.create_user = create_user
        self.update_user = create_user
        self.request_header = request_header
        self.request_method = request_method
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

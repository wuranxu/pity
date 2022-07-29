from datetime import datetime

from sqlalchemy import INT, Column, TIMESTAMP, String, BIGINT
from sqlalchemy.dialects.mysql import SMALLINT

from app.models import Base


class PityReport(Base):
    __tablename__ = 'pity_report'
    id = Column(INT, primary_key=True)
    # 执行人 0则为CPU
    executor = Column(INT, index=True)

    # 环境
    env = Column(INT, nullable=False)
    # 花费时间
    cost = Column(String(8))
    # 测试集合id，预留字段
    plan_id = Column(INT, index=True, nullable=True)
    # 开始时间
    start_at = Column(TIMESTAMP, nullable=False)
    # 结束时间
    finished_at = Column(TIMESTAMP)
    # 成功数量
    success_count = Column(INT, nullable=False, default=0)
    error_count = Column(INT, nullable=False, default=0)
    failed_count = Column(INT, nullable=False, default=0)
    skipped_count = Column(INT, nullable=False, default=0)

    # 执行状态
    status = Column(SMALLINT, nullable=False, comment="0: pending, 1: running, 2: stopped, 3: finished", index=True)

    # case执行模式
    mode = Column(SMALLINT, default=0, comment="0: 普通, 1: 测试集, 2: pipeline, 3: 其他")

    deleted_at = Column(BIGINT, nullable=False, default=0)

    def __init__(self, executor: int, env: int, success_count: int = 0, failed_count: int = 0,
                 error_count: int = 0, skipped_count: int = 0, status: int = 0, mode: int = 0,
                 plan_id: int = None, finished_at: datetime = None, cost=None):
        self.executor = executor
        self.env = env
        self.start_at = datetime.now()
        self.success_count = success_count
        self.cost = cost
        self.failed_count = failed_count
        self.error_count = error_count
        self.skipped_count = skipped_count
        self.mode = mode
        self.status = status
        self.plan_id = plan_id
        self.finished_at = finished_at
        self.deleted_at = 0

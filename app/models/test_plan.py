from sqlalchemy import Column, String, TEXT, UniqueConstraint, BOOLEAN, SMALLINT, INT
from sqlalchemy.dialects.mysql import TINYTEXT

from app.models.basic import PityBase


class PityTestPlan(PityBase):
    project_id = Column(INT, nullable=False)
    # 测试计划执行环境, 可以多选
    env = Column(String(64), nullable=False)
    # 测试计划名称
    name = Column(String(32), nullable=False)
    # 测试计划优先级
    priority = Column(String(3), nullable=False)
    # cron表达式
    cron = Column(String(12), nullable=False)
    # 用例列表
    case_list = Column(TEXT, nullable=False)
    # 并行/串行(是否顺序执行)
    ordered = Column(BOOLEAN, default=False)
    # 通过率低于这个数会自动发通知
    pass_rate = Column(SMALLINT, default=80)
    # 通知用户，目前只有邮箱，后续用户表可能要完善手机号字段，为了通知
    receiver = Column(TEXT)
    # 通知方式 0: 邮件 1: 钉钉 2: 企业微信 3: 飞书 支持多选
    msg_type = Column(TINYTEXT)
    # 单次case失败重试间隔，默认2分钟
    retry_minutes = Column(SMALLINT, default=2)
    # 测试计划是否正在执行中
    state = Column(SMALLINT, default=0, comment="0: 未开始 1: 运行中")

    __table_args__ = (
        UniqueConstraint('project_id', 'name', 'deleted_at'),
    )

    __tablename__ = "pity_test_plan"

    def __init__(self, project_id, env, case_list, name, priority, cron, ordered, pass_rate, receiver, msg_type,
                 retry_minutes, user, state=0, id=None):
        super().__init__(user, id)
        self.env = ",".join(map(str, env))
        self.case_list = ",".join(map(str, case_list))
        self.name = name
        self.project_id = project_id
        self.priority = priority
        self.ordered = ordered
        self.cron = cron
        self.pass_rate = pass_rate
        self.receiver = ",".join(map(str, receiver))
        self.msg_type = ",".join(map(str, msg_type))
        self.retry_minutes = retry_minutes
        self.state = state

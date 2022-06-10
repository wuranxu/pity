from sqlalchemy import Column, String, TEXT, UniqueConstraint, BOOLEAN, SMALLINT, INT

from app.models.basic import PityBase

_notice_type = {
    '0': '邮件',
    '1': '钉钉',
    '2': '企业微信',
    '3': '飞书'
}


class PityTestPlan(PityBase):
    project_id = Column(INT, nullable=False)
    # 测试计划执行环境, 可以多选
    env = Column(String(64), nullable=False)
    # 测试计划名称
    name = Column(String(32), nullable=False)
    # 测试计划优先级
    priority = Column(String(3), nullable=False)
    # cron表达式
    cron = Column(String(24), nullable=False)
    # 用例列表
    case_list = Column(TEXT, nullable=False)
    # 并行/串行(是否顺序执行)
    ordered = Column(BOOLEAN, default=False)
    # 通过率低于这个数会自动发通知
    pass_rate = Column(SMALLINT, default=80)
    # 通知用户，目前只有邮箱，后续用户表可能要完善手机号字段，为了通知
    receiver = Column(TEXT)
    # 通知方式 0: 邮件 1: 钉钉 2: 企业微信 3: 飞书 支持多选
    msg_type = Column(TEXT)
    # 单次case失败重试间隔，默认2分钟
    retry_minutes = Column(SMALLINT, nullable=False, default=0)
    # 测试计划是否正在执行中
    state = Column(SMALLINT, default=0, comment="0: 未开始 1: 运行中")

    __table_args__ = (
        UniqueConstraint('project_id', 'name', 'deleted_at'),
    )

    __tablename__ = "pity_test_plan"

    __fields__ = (name, project_id, env, priority)
    __tag__ = "测试计划"
    __alias__ = dict(name="名称", project_id="项目", env="环境", priority="优先级", cron="cron", ordered="顺序",
                     pass_rate="通过率", msg_type="通知类型", retry_minutes="重试时间", receiver="通知人", case_list="用例列表")

    def __init__(self, project_id, env, case_list, name, priority, cron, ordered, pass_rate, receiver, msg_type,
                 user, state=0, retry_minutes=0, id=None):
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

    @staticmethod
    def get_msg_type(msg_type):
        return ",".join(_notice_type.get(str(x), '未知') for x in msg_type.split(","))

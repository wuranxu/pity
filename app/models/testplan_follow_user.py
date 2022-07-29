from sqlalchemy import INT, Column, UniqueConstraint

from app.models.basic import PityBase


class PityTestPlanFollowUserRel(PityBase):
    """
    测试计划关注用户表
    """
    __tablename__ = "pity_testplan_follow_user_rel"
    __table_args__ = (
        UniqueConstraint('user_id', 'plan_id', 'deleted_at'),
    )

    user_id = Column(INT, nullable=False)
    plan_id = Column(INT, nullable=False)

    def __init__(self, plan_id, user_id):
        super().__init__(user_id)
        self.user_id = user_id
        self.plan_id = plan_id

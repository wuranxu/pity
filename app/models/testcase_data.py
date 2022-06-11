"""
测试数据表, 用来存储各个环境下的测试数据，用于数据驱动
"""
__author__ = "miluo"

from sqlalchemy import Column, INT, String, UniqueConstraint, TEXT

from app.models.basic import PityBase


class PityTestcaseData(PityBase):
    env = Column(INT, nullable=False)
    case_id = Column(INT, nullable=False)
    name = Column(String(32), nullable=False)
    json_data = Column(TEXT, nullable=False)

    __table_args__ = (
        UniqueConstraint('env', 'case_id', 'name', 'deleted_at'),
    )

    __tablename__ = "pity_testcase_data"

    __fields__ = [name]
    __show__ = 1

    def __init__(self, env, case_id, name, json_data, user_id, id=None):
        super().__init__(user_id, id)
        self.env = env
        self.case_id = case_id
        self.name = name
        self.json_data = json_data

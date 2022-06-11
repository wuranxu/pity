from typing import Tuple

from sqlalchemy import Column, String, UniqueConstraint

from app.models.basic import PityBase


class Environment(PityBase):
    __tablename__ = 'pity_environment'
    # 环境名称
    name = Column(String(10))
    remarks = Column(String(200))

    __table_args__ = (
        UniqueConstraint('name', 'deleted_at'),
    )

    __fields__ = [name]
    __tag__ = "环境"
    __alias__ = dict(name="名称", remarks="备注")

    def __init__(self, name, remarks, user, id=None):
        super().__init__(user, id)
        self.name = name
        self.remarks = remarks

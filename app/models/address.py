"""
数据构造器表, 包含前置条件和后置条件
"""

from sqlalchemy import Column, INT, String, UniqueConstraint

from app.models.basic import PityBase


class PityAddress(PityBase):
    __tablename__ = 'pity_gateway'
    __table_args__ = (
        UniqueConstraint('env', 'name', 'deleted_at'),
    )
    env = Column(INT, comment='对应环境')
    name = Column(String(32), comment="网关名称")
    gateway = Column(String(128), comment="网关地址")

    def __init__(self, env, name, gateway, user, id=None):
        super().__init__(user, id)
        self.name = name
        self.env = env
        self.gateway = gateway

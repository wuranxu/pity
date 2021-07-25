"""
数据构造器表
"""
from datetime import datetime

from sqlalchemy import Column, INT, DATETIME, String, BOOLEAN, UniqueConstraint, TEXT

from app.models import Base


class Constructor(Base):
    __tablename__ = 'pity_constructor'
    __table_args__ = (
        UniqueConstraint('case_id', 'name', 'deleted_at'),
    )

    id = Column(INT, primary_key=True)
    deleted_at = Column(DATETIME)
    created_at = Column(DATETIME, nullable=False)
    updated_at = Column(DATETIME, nullable=False)
    create_user = Column(INT, nullable=True)
    update_user = Column(INT, nullable=True)
    type = Column(INT, default=0, comment="0: testcase 1: sql 2: redis 3: 待完善")
    name = Column(String(64), comment="数据初始化描述")
    enable = Column(BOOLEAN, default=True, nullable=False)
    constructor_json = Column(TEXT, nullable=False)
    value = Column(String(16), comment="返回值")
    case_id = Column(INT, nullable=False, comment="所属用例id")
    public = Column(BOOLEAN, default=False, comment="是否共享")

    def __init__(self, type, name, enable, constructor_json, case_id, public, user, value="", id=0):
        self.id = id
        self.type = type
        self.name = name
        self.enable = enable
        self.constructor_json = constructor_json
        self.case_id = case_id
        self.public = public
        self.value = value
        self.update_user = user
        self.create_user = user
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

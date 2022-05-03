from datetime import datetime

from sqlalchemy import Column, String, INT, TIMESTAMP, Boolean, BIGINT

from app.models import Base


class User(Base):
    __tablename__ = "pity_user"

    id = Column(INT, primary_key=True)
    username = Column(String(16), unique=True, index=True)
    name = Column(String(16), index=True)
    password = Column(String(32), unique=False)
    email = Column(String(64), unique=True, nullable=False)
    role = Column(INT, default=0, comment="0: 普通用户 1: 组长 2: 超级管理员")
    phone = Column(String(12), unique=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    deleted_at = Column(BIGINT, nullable=False, default=0)
    update_user = Column(INT, nullable=True)  # 修改人
    last_login_at = Column(TIMESTAMP)
    avatar = Column(String(128), nullable=True, default=None)
    # 管理员可以禁用某个用户，当他离职后
    is_valid = Column(Boolean, nullable=False, default=True, comment="是否合法")

    def __init__(self, username, name, password, email, avatar=None, phone=None, is_valid=True):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.role = 0
        self.phone = phone
        self.avatar = avatar
        self.is_valid = is_valid
        self.deleted_at = 0

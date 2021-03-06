from datetime import datetime

from sqlalchemy import Column, String, INT, DATETIME

from app.models import Base


class User(Base):
    __tablename__ = "pity_user"

    id = Column(INT, primary_key=True)
    username = Column(String(16), unique=True, index=True)
    name = Column(String(16), index=True)
    password = Column(String(32), unique=False)
    email = Column(String(64), unique=True, nullable=False)
    role = Column(INT, default=0, comment="0: 普通用户 1: 组长 2: 超级管理员")
    created_at = Column(DATETIME, nullable=False)
    updated_at = Column(DATETIME, nullable=False)
    deleted_at = Column(DATETIME)
    last_login_at = Column(DATETIME)
    avatar = Column(String(128), nullable=True, default=None)

    def __init__(self, username, name, password, email, avatar=None):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.role = 0
        self.avatar = avatar

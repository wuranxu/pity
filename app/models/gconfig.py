from datetime import datetime

from sqlalchemy import INT, DATETIME, Column, String, TEXT, BOOLEAN, UniqueConstraint

from app.models import Base


class GConfig(Base):
    __tablename__ = 'pity_gconfig'
    id = Column(INT, primary_key=True)
    env = Column(INT)
    key = Column(String(16))
    value = Column(TEXT)
    key_type = Column(INT, nullable=False, comment="0: string 1: json 2: yaml")
    # 是否可用
    enable = Column(BOOLEAN, default=True)
    created_at = Column(DATETIME, nullable=False)
    updated_at = Column(DATETIME, nullable=False)
    deleted_at = Column(DATETIME)
    create_user = Column(INT, nullable=True)
    update_user = Column(INT, nullable=True)

    __table_args__ = (
        UniqueConstraint('env', 'key', 'deleted_at'),
    )

    def __init__(self, env, key, value, key_type, enable, user, id=0):
        self.id = id
        self.env = env
        self.key = key
        self.value = value
        self.key_type = key_type
        self.enable = enable
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.create_user = user
        self.update_user = user

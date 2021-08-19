from datetime import datetime

from sqlalchemy import INT, DATETIME, Column, String, UniqueConstraint

from app.models import Base


class PityDatabase(Base):
    __tablename__ = "pity_database_info"
    __table_args__ = (
        UniqueConstraint('env', 'name', 'deleted_at'),
    )

    id = Column(INT, primary_key=True)
    env = Column(INT, nullable=False)  # 对应环境id
    name = Column(String(24), nullable=False)  # 数据库描述名称
    host = Column(String(64), nullable=False)  # 防止超长域名出现
    port = Column(INT, nullable=False)
    username = Column(String(36), nullable=False)
    password = Column(String(64), nullable=False)
    database = Column(String(36), nullable=False)
    sql_type = Column(INT, nullable=False, comment="0: mysql 1: postgresql 2: mongo")
    created_at = Column(DATETIME, nullable=False)
    updated_at = Column(DATETIME, nullable=False)
    deleted_at = Column(DATETIME)
    create_user = Column(INT, nullable=True)
    update_user = Column(INT, nullable=True)

    def __init__(self, env, name, host, port, username, password, database, sql_type, user, id=0):
        self.id = id
        self.env = env
        self.name = name
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.sql_type = sql_type
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.create_user = user
        self.update_user = user

from sqlalchemy import Column, INT, String, Boolean, UniqueConstraint

from app.models.basic import PityBase


class PityRedis(PityBase):
    __tablename__ = "pity_redis_info"
    __table_args__ = (
        UniqueConstraint('env', 'name', 'deleted_at'),
    )

    env = Column(INT, nullable=False)  # 对应环境id
    name = Column(String(24), nullable=False)  # redis描述名称
    addr = Column(String(128), nullable=False)
    username = Column(String(36), nullable=False)
    password = Column(String(64), nullable=False)
    db = Column(INT, nullable=False)
    # 是否是集群，默认为false，集群可不输入用户密码
    cluster = Column(Boolean, default=False, nullable=False)

    def __init__(self, env, name, addr, username, password, db, cluster, user, id=None):
        super().__init__(user, id=id)
        self.env = env
        self.name = name
        self.addr = addr
        self.password = password
        self.username = username
        self.db = db
        self.cluster = cluster

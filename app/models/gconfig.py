from sqlalchemy import INT, Column, String, TEXT, BOOLEAN, UniqueConstraint

from app.models.basic import PityBase


class GConfig(PityBase):
    __tablename__ = 'pity_gconfig'
    env = Column(INT)
    key = Column(String(16))
    value = Column(TEXT)
    key_type = Column(INT, nullable=False, comment="0: string 1: json 2: yaml")
    # 是否可用
    enable = Column(BOOLEAN, default=True)

    __table_args__ = (
        UniqueConstraint('env', 'key', 'deleted_at'),
    )

    __fields__ = (env, key)
    __tag__ = "全局变量"
    __alias__ = dict(env="环境", key="名称", key_type="类型", value="值")
    __show__ = 2

    def __init__(self, env, key, value, key_type, enable, user, id=None):
        super().__init__(user, id)
        self.env = env
        self.key = key
        self.value = value
        self.key_type = key_type
        self.enable = enable

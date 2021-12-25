from datetime import datetime

from sqlalchemy import INT, DATETIME, Column, BIGINT

from app.models import Base
from config import Config


class PityBase(Base):
    id = Column(INT, primary_key=True)
    created_at = Column(DATETIME, nullable=False)
    updated_at = Column(DATETIME, nullable=False)
    deleted_at = Column(BIGINT, nullable=False, default=0)
    create_user = Column(INT, nullable=False)
    update_user = Column(INT, nullable=False)
    __abstract__ = True
    __fields__ = (id,)
    __tag__ = "未定义"
    __alias__ = dict(name="名称")
    __show__ = 1

    def __init__(self, user, id=None):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.create_user = user
        self.update_user = user
        self.deleted_at = 0
        self.id = id


class PityRelationField(object):
    def __init__(self, field, foreign=None):
        self.field = field
        self.foreign = foreign


def init_relation(model, *data: PityRelationField):
    setattr(model, Config.RELATION, data)

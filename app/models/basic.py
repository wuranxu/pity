from datetime import datetime

from sqlalchemy import INT, DATETIME, Column, BIGINT

from app.models import Base


class PityBase(Base):
    id = Column(INT, primary_key=True)
    created_at = Column(DATETIME, nullable=False)
    updated_at = Column(DATETIME, nullable=False)
    deleted_at = Column(BIGINT, nullable=False, default=0)
    create_user = Column(INT, nullable=False)
    update_user = Column(INT, nullable=False)
    __abstract__ = True

    def __init__(self, user, id=0):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.create_user = user
        self.update_user = user
        self.id = id

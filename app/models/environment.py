from datetime import datetime

from sqlalchemy import INT, DATETIME, Column, String, UniqueConstraint

from app.models import Base


class Environment(Base):
    __tablename__ = 'pity_environment'
    id = Column(INT, primary_key=True)
    # 环境名称
    name = Column(String(10))
    created_at = Column(DATETIME, nullable=False)
    updated_at = Column(DATETIME, nullable=False)
    deleted_at = Column(DATETIME)
    create_user = Column(INT, nullable=True)
    update_user = Column(INT, nullable=True)
    remarks = Column(String(200))

    __table_args__ = (
        UniqueConstraint('name', 'deleted_at'),
    )

    def __init__(self, name, remarks, user, id=0):
        self.id = id
        self.create_user = user
        self.name = name
        self.remarks = remarks
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.update_user = user

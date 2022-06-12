from datetime import datetime

from sqlalchemy import Column, INT, TIMESTAMP, String, SMALLINT, TEXT

from app.enums.OperationEnum import OperationType
from app.models import Base


class PityOperationLog(Base):
    """
    用户操作记录表
    """
    __tablename__ = 'pity_operation_log'

    id = Column(INT, primary_key=True)
    # 操作人
    user_id = Column(INT, index=True)

    # 操作时间
    operate_time = Column(TIMESTAMP)

    # 操作title
    title = Column(String(128), nullable=False)

    # 操作描述
    description = Column(TEXT, comment="操作描述")

    # tag
    tag = Column(String(24), comment="操作tag")

    # mode
    mode = Column(SMALLINT, comment="操作类型")

    # key
    key = Column(INT, nullable=True, comment="关键id，可能是目录id，case_id或者其他id")

    def __init__(self, user_id, mode: OperationType, title, tag, description, key=None):
        self.user_id = user_id
        self.tag = tag
        self.mode = mode.value
        self.title = title
        self.key = key
        self.description = description
        self.operate_time = datetime.now()

from datetime import datetime

from sqlalchemy import Column, INT, TIMESTAMP, BIGINT

from app.models import Base


class PityBroadcastReadUser(Base):
    id = Column(BIGINT, primary_key=True)
    notification_id = Column(INT, comment="对应消息id", index=True)
    read_user = Column(INT, comment="已读用户id")
    read_time = Column(TIMESTAMP, comment="已读时间")

    __tablename__ = "pity_broadcast_read_user"

    def __init__(self, notification_id: int, read_user: int):
        self.notification_id = notification_id
        self.read_user = read_user
        self.read_time = datetime.now()
        self.id = None

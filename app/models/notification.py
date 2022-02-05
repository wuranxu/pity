from sqlalchemy import SMALLINT, Column, VARCHAR, INT

from app.models.basic import PityBase


class PityNotification(PityBase):
    msg_type = Column(SMALLINT, comment="消息类型 1: 系统消息 2: 其他消息")
    msg_title = Column(VARCHAR(32), comment="消息标题", nullable=False)
    msg_content = Column(VARCHAR(200), comment="消息内容", nullable=True)
    msg_link = Column(VARCHAR(128), comment="消息链接")
    msg_status = Column(SMALLINT, comment="消息状态 1: 未读 2: 已读")
    sender = Column(INT, comment="消息发送人, 0则是CPU 非0则是其他用户")
    receiver = Column(INT, comment="消息接收人, 系统消息则该字段为空")

    __tablename__ = "pity_notification"

    def __init__(self, msg_type, msg_title, msg_content, sender, receiver, user, msg_link=None, msg_status=0):
        super().__init__(user)
        self.msg_type = msg_type
        self.msg_title = msg_title
        self.receiver = receiver
        self.msg_content = msg_content
        self.sender = sender
        self.msg_link = msg_link
        self.msg_status = msg_status

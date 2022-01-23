from sqlalchemy import SMALLINT, Column, VARCHAR, INT

from app.models.basic import PityBase


class PityNotification(PityBase):
    msg_type = Column(SMALLINT, comment="消息类型 0: 用例执行 1: 任务分配")
    msg_content = Column(VARCHAR(200), comment="消息内容", nullable=True)
    msg_link = Column(VARCHAR(128), comment="消息链接")
    msg_status = Column(SMALLINT, comment="消息状态 0: 未读 1: 已读")
    sender = Column(INT, comment="消息发送人, 0则是CPU 非0则是其他用户")
    receiver = Column(INT, comment="消息接收人, 0为广播消息")

    __tablename__ = "pity_notification"

    def __init__(self, msg_type, msg_content, sender, receiver, user, msg_link=None, msg_status=0):
        super().__init__(user)
        self.msg_type = msg_type
        self.receiver = receiver
        self.msg_content = msg_content
        self.sender = sender
        self.msg_link = msg_link
        self.msg_status = msg_status

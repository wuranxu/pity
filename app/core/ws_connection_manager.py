# import abc
from typing import TypeVar

from fastapi import WebSocket

from app.core.msg.wss_msg import WebSocketMessage
from app.crud.notification.NotificationDao import PityNotificationDao
from app.models.notification import PityNotification
from app.utils.logger import Log

MsgType = TypeVar('MsgType', str, dict, bytes)


# class MsgSender(metaclass=abc.ABCMeta):
#     @abc.abstractmethod
#     def send_text(self):
#         pass
#
#     @abc.abstractmethod
#     def send_json(self):
#         pass
#
#     @abc.abstractmethod
#     def send_bytes(self):
#         pass


class ConnectionManager:
    BROADCAST = -1
    logger = Log("wss_manager")

    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}
        self.log = Log("websocket")

    def get_clients(self):
        return {key: True for key in self.active_connections.keys()}

    async def connect(self, websocket: WebSocket, client_id: int) -> None:
        await websocket.accept()
        exist: WebSocket = self.active_connections.get(client_id)
        if exist:
            await exist.close()
            self.active_connections[client_id]: WebSocket = websocket
        else:
            self.active_connections[client_id]: WebSocket = websocket
            self.log.debug(F"websocket: 用户[{client_id}]建立连接成功！")

    def disconnect(self, client_id: int) -> None:
        del self.active_connections[client_id]
        self.log.debug(F"websocket: 用户[{client_id}] 已安全断开！")

    @staticmethod
    async def pusher(sender: WebSocket, message: MsgType) -> None:
        """
        根据不同的消息类型，调用不同方法发送消息
        """
        msg_mapping: dict = {
            str: sender.send_text,
            dict: sender.send_json,
            bytes: sender.send_bytes
        }
        func_push_msg = msg_mapping.get(type(message))
        if func_push_msg:
            await func_push_msg(message)
        else:
            raise TypeError(F"websocket不能发送{type(message)}的内容！")

    async def send_personal_message(self, user_id: int, message: MsgType) -> None:
        """
        发送个人信息
        """
        conn = self.active_connections.get(user_id)
        if conn:
            await self.pusher(sender=conn, message=message)

    async def broadcast(self, message: MsgType) -> None:
        """
        广播
        """
        for connection in self.active_connections.values():
            await self.pusher(sender=connection, message=message)

    async def send_data(self, user_id, msg_type, record_msg):
        msg = dict(type=msg_type, record_msg=record_msg)
        await self.send_personal_message(user_id, msg)

    async def notify(self, user_id, title=None, content=None, notice: PityNotification = None):
        """
        根据user_id推送对应的
        :param content:
        :param title:
        :param user_id: 当user_id为-1的时候代表是广播消息
        :param notice:
        :return:
        """
        try:
            # 判断是否为桌面通知
            if title is not None:
                msg = WebSocketMessage.desktop_msg(title, content)
                if user_id == ConnectionManager.BROADCAST:
                    await self.broadcast(msg)
                else:
                    await self.send_personal_message(user_id, msg)
            else:
                # 说明不是桌面消息，直接给出消息数量即可
                if user_id == ConnectionManager.broadcast:
                    await self.broadcast(WebSocketMessage.msg_count())
                else:
                    await self.send_personal_message(user_id, WebSocketMessage.msg_count())
            # 判断是否要落入推送表
            if notice is not None:
                await PityNotificationDao.insert(model=notice)
        except Exception as e:
            ConnectionManager.logger.error(f"发送消息失败, {e}")


ws_manage = ConnectionManager()

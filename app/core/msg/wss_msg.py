from app.enums.MessageEnum import WebSocketMessageEnum


class WebSocketMessage(object):

    @staticmethod
    def msg_count(count=1, total=False):
        return dict(type=WebSocketMessageEnum.COUNT, count=count, total=total)

    @staticmethod
    def desktop_msg(title, content=''):
        return dict(type=WebSocketMessageEnum.DESKTOP, title=title, content=content)

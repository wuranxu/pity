# 通知类型
from enum import IntEnum


class NoticeType(IntEnum):
    EMAIL = 0
    DINGDING = 1
    WECHAT = 2
    FEISHU = 3

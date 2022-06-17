# 1: 调试中 2: 暂时关闭 3: 正常运作
from enum import IntEnum


class CaseStatus(IntEnum):
    debugging = 1
    closed = 2
    running = 3

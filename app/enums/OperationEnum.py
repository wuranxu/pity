# 日志类型
from enum import IntEnum


class OperationType(IntEnum):
    INSERT = 0
    UPDATE = 1
    DELETE = 2
    EXECUTE = 3
    STOP = 4

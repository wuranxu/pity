from enum import IntEnum


class DatabaseEnum(IntEnum):
    """
    数据库类型枚举
    """
    MYSQL = 0  # mysql
    POSTGRESQL = 1  # pg

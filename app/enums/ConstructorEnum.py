# 前置条件类型
from enum import IntEnum


class ConstructorType(IntEnum):
    testcase = 0
    sql = 1
    redis = 2
    py_script = 3
    http = 4

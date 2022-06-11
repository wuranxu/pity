# 请求类型
from enum import IntEnum


class BodyType(IntEnum):
    none = 0
    json = 1
    form = 2
    x_form = 3
    binary = 4
    graphQL = 5

from enum import IntEnum


class GConfigParserEnum(IntEnum):
    string = 0
    json = 1
    yaml = 2


class GconfigType(IntEnum):
    case = 0
    constructor = 1
    asserts = 2

    @staticmethod
    def text(val):
        if val == 0:
            return "用例"
        if val == 1:
            return "前后置条件"
        return "断言"

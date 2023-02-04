from enum import IntEnum


class CaseParametersEnum(IntEnum):
    TEXT = 0
    JSON = 1
    HEADER = 2
    COOKIE = 3
    STATUS_CODE = 4
    BODY_REGEX = 5
    BODY_JSON = 6
    REQUEST_HEADER = 7

from app.core.paramters.jsonpath_parser import JSONPathParser
from app.core.paramters.kv_parser import KvParser
from app.core.paramters.regex_parser import RegexParser
from app.core.paramters.status_code_parser import StatusCodeParser
from app.enums.CaseParametersEnum import CaseParametersEnum


def ParametersParser(parameter_type: CaseParametersEnum):
    if parameter_type == CaseParametersEnum.TEXT:
        return RegexParser.parse
    if parameter_type == CaseParametersEnum.JSON:
        return JSONPathParser.parse
    if parameter_type in (CaseParametersEnum.HEADER, CaseParametersEnum.COOKIE):
        return KvParser.parse
    return StatusCodeParser.parse

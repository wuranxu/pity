from app.core.paramters.jsonpath_parser import JSONPathParser, BodyJSONPathParser
from app.core.paramters.kv_parser import HeaderParser, CookieParser, RequestHeaderParser
from app.core.paramters.regex_parser import RegexParser, BodyRegexParser
from app.core.paramters.status_code_parser import StatusCodeParser
from app.enums.CaseParametersEnum import CaseParametersEnum


def parameters_parser(parameter_type: CaseParametersEnum):
    if parameter_type == CaseParametersEnum.TEXT:
        return RegexParser.parse
    if parameter_type == CaseParametersEnum.BODY_REGEX:
        return BodyRegexParser.parse
    if parameter_type == CaseParametersEnum.JSON:
        return JSONPathParser.parse
    if parameter_type == CaseParametersEnum.BODY_JSON:
        return BodyJSONPathParser.parse
    if parameter_type == CaseParametersEnum.HEADER:
        return HeaderParser.parse
    if parameter_type == CaseParametersEnum.COOKIE:
        return CookieParser.parse
    if parameter_type == CaseParametersEnum.REQUEST_HEADER:
        return RequestHeaderParser.parse
    return StatusCodeParser.parse

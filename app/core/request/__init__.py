from app.core.request.convertor import Convertor
from app.core.request.har_convertor import HarConvertor
from app.enums.ConvertorEnum import CaseConvertorType


def get_convertor(c: CaseConvertorType) -> (Convertor.convert, str):
    if c == CaseConvertorType.har:
        return HarConvertor.convert, CaseConvertorType.har.name
    return None, ""

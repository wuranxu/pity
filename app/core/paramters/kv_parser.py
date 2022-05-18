from typing import Any

import jsonpath

from app.core.paramters.parser import Parser
from app.excpetions.CaseParametersException import CaseParametersException


class KvParser(Parser):

    @staticmethod
    def parse(source: dict, expression: str = "", idx: int = None) -> Any:
        if not source or not expression:
            raise CaseParametersException(f"parse out parameters failed, source or expression is empty")
        try:
            return jsonpath.jsonpath(source, expression)
        except CaseParametersException as e:
            raise e
        except Exception as err:
            raise CaseParametersException(f"parse json data error, please check jsonpath or json: {err}")

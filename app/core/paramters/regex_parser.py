"""
regex for text
"""
import re
from typing import Any

from app.core.paramters.parser import Parser
from app.exception.error import CaseParametersError


class RegexParser(Parser):

    @staticmethod
    def parse(source: dict, expression: str = "", idx: str = None) -> Any:
        try:
            source = source.get("response")
            if not source or not expression:
                raise CaseParametersError(f"parse out parameters failed, source or expression is empty")
            if idx is None:
                raise CaseParametersError("index is empty, you must provide index for regex match results.")
            pattern = re.compile(expression)
            result = re.findall(pattern, source)
            if len(result) == 0:
                raise CaseParametersError(f"regex match failed, please check your regex: {expression}")
            return Parser.parse_result(result, idx)
        except CaseParametersError as e:
            raise e
        except Exception as err:
            raise CaseParametersError(f"parse regex text error, please check regex or text: {err}")

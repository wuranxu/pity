"""
regex for text
"""
import re
from typing import Any

from app.core.paramters.parser import Parser
from app.excpetions.CaseParametersException import CaseParametersException


class RegexParser(Parser):

    @staticmethod
    def parse(source: str, expression: str="", idx: int = None) -> Any:
        try:
            if not source or not expression:
                raise CaseParametersException(f"parse out parameters failed, source or expression is empty")
            if idx is None:
                raise CaseParametersException("index is empty, you must provide index for regex match results.")
            pattern = re.compile(expression)
            result = re.findall(pattern, source)
            length = len(result)
            if idx >= length or idx < -length:
                raise CaseParametersException(f"results length is {length}, index is not in [{-length}, {length})")
            return result[idx]
        except CaseParametersException as e:
            raise e
        except Exception as err:
            raise CaseParametersException(f"parse regex text error, please check regex or text: {err}")

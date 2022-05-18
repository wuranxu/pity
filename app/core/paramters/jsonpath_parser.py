"""
jsonpath parser
"""
import json
from functools import lru_cache
from typing import Any

import jsonpath

from app.core.paramters.parser import Parser
from app.excpetions.CaseParametersException import CaseParametersException


class JSONPathParser(Parser):

    @staticmethod
    def parse(source: str, expression: str = "", idx: int = None) -> Any:
        if not source or not expression:
            raise CaseParametersException(f"parse out parameters failed, source or expression is empty")
        data = JSONPathParser.get_object(source)
        try:
            return jsonpath.jsonpath(data, expression)
        except CaseParametersException as e:
            raise e
        except Exception as err:
            raise CaseParametersException(f"parse json data error, please check jsonpath or json: {err}")

    @staticmethod
    @lru_cache()
    def get_object(json_str):
        return json.loads(json_str)

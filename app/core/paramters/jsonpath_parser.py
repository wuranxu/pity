"""
jsonpath parser
"""
import json
from functools import lru_cache
from typing import Any

import jsonpath

from app.core.paramters.parser import Parser
from app.exception.error import CaseParametersError


class JSONPathParser(Parser):

    @staticmethod
    def parse(source: dict, expression: str = "", **kwargs) -> Any:
        source = source.get("response")
        if not source or not expression:
            raise CaseParametersError(f"parse out parameters failed, source or expression is empty")
        try:
            data = JSONPathParser.get_object(source)
            results = jsonpath.jsonpath(data, expression)
            if results is False:
                if not data and expression == "$..*":
                    # 说明想要全匹配并且没数据，直接返回data
                    return json.dumps(data, ensure_ascii=False)
                raise CaseParametersError("jsonpath match failed, please check your response or jsonpath.")
            return Parser.parse_result(results, "0")
        except CaseParametersError as e:
            raise e
        except Exception as err:
            raise CaseParametersError(f"parse json data error, please check jsonpath or json: {err}")

    @staticmethod
    @lru_cache()
    def get_object(json_str):
        return json.loads(json_str)

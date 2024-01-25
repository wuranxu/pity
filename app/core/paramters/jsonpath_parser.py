"""
jsonpath parser
"""
import json
from typing import Any

import jsonpath

from app.core.paramters.parser import Parser
from app.exception.error import CaseParametersError


class JSONPathParser(Parser):

    @classmethod
    def get_source(cls, source):
        return source.get("response")

    @classmethod
    def parse(cls, source: dict, expression: str = "", **kwargs) -> Any:
        data = cls.get_source(source)
        if not source or not expression:
            raise CaseParametersError(f"parse out parameters failed, source or expression is empty")
        try:
            results = jsonpath.jsonpath(data, expression)
            if results is False:
                if not data and expression == "$..*":
                    # 说明想要全匹配并且没数据，直接返回data
                    return data
                raise CaseParametersError("jsonpath match failed, please check your response or jsonpath.")
            return Parser.parse_result(results, "0")
        except CaseParametersError as e:
            raise e
        except Exception as err:
            raise CaseParametersError(f"parse json data error, please check jsonpath or json: {err}")


class BodyJSONPathParser(JSONPathParser):
    @classmethod
    def get_source(cls, source):
        return source.get("request_data")

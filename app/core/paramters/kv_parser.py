import json
from typing import Any

import jsonpath

from app.core.paramters.parser import Parser
from app.exception.error import CaseParametersError


class HeaderParser(Parser):

    @staticmethod
    def get_source(data: dict):
        return json.loads(data.get("response_headers"))

    @classmethod
    def parse(cls, source: dict, expression: str = "", idx: str = None) -> Any:
        if not source or not expression:
            raise CaseParametersError(f"parse out parameters failed, source or expression is empty")
        try:
            source = cls.get_source(source)
            results = jsonpath.jsonpath(source, expression)
            if results is False:
                if not source and expression == "$..*":
                    # 说明想要全匹配并且没数据，直接返回data
                    return source
                raise CaseParametersError("jsonpath match failed, please check your response or jsonpath.")
            return Parser.parse_result(results, idx)
        except CaseParametersError as e:
            raise e
        except Exception as err:
            raise CaseParametersError(f"parse json data error, please check jsonpath or json: {err}")


class CookieParser(HeaderParser):
    @staticmethod
    def get_source(data: dict):
        return json.loads(data.get("cookies"))

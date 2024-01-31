import json
import random
from typing import Any

from app.exception.error import CaseParametersError


class Parser(object):

    @staticmethod
    def parse(source: dict, expression: str = "", **kwargs) -> Any:
        raise NotImplementedError

    @staticmethod
    def parse_result(data: list, match_index: str = None):
        if len(data) == 0:
            return None
        # 如果是数字
        length = len(data)
        if match_index is not None:
            if match_index.isdigit():
                idx = int(match_index)
                if idx >= length or idx < -length:
                    raise CaseParametersError(f"results length is {length}, index is not in [{-length}, {length})")
                return data[idx]
            if match_index.lower() == 'random':
                # 随机选取
                return random.choice(data)
            if match_index.lower() == 'all':
                return data
            raise CaseParametersError(f"invalid match index: {match_index}, not number or random")
        return data[0]

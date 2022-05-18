from typing import Any


class Parser(object):

    @staticmethod
    def parse(source: str, expression: str = "", idx: int = None) -> Any:
        raise NotImplementedError

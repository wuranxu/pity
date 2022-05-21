import json

from app.core.paramters.parser import Parser


class StatusCodeParser(Parser):
    @staticmethod
    def parse(source: dict, expression: str = "", idx: str = None) -> str:
        return json.dumps(source.get("status_code"))

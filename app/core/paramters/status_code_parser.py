from app.core.paramters.parser import Parser


class StatusCodeParser(Parser):
    @staticmethod
    def parse(source: dict, expression: str = "", idx: int = None) -> int:
        return source.get("status_code")

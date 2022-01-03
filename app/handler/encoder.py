import json
from datetime import datetime
from typing import Any


class JsonEncoder(json.JSONEncoder):

    def default(self, o: Any) -> Any:
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        return self.default(o)

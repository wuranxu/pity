from pydantic import BaseModel, validator

from app.enums.RequestBodyEnum import BodyType
from app.exception.error import ParamsError


class HttpRequestForm(BaseModel):
    method: str
    url: str
    body: str = None
    body_type: BodyType = BodyType.none
    headers: dict = {}

    @validator('method', 'url')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v

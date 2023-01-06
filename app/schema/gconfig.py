from pydantic import BaseModel, validator

from app.exception.error import ParamsError


class GConfigForm(BaseModel):
    id: int = None
    key: str
    value: str
    env: str = None
    key_type: int
    enable: bool

    @validator("key", "value", "key_type", "enable")
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        if not isinstance(v, int):
            if not v:
                raise ParamsError("不能为空")
        return v

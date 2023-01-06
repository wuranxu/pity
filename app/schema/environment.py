from pydantic import BaseModel, validator

from app.exception.error import ParamsError


class EnvironmentForm(BaseModel):
    id: int = None
    name: str
    remarks: str = None

    @validator("name")
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v

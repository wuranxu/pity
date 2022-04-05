from pydantic import BaseModel, validator

from app.excpetions.ParamsException import ParamsError
from app.schema.base import PityModel


class TestCaseForm(BaseModel):
    id: int = None
    priority: str
    url: str
    name: str
    case_type: int = 0
    base_path: str = None
    tag: str = None
    body: str = None
    body_type: int = 0
    request_headers: str = None
    request_method: str = None
    status: int
    directory_id: int
    request_type: int

    @validator("priority", "status", "directory_id", "request_type", "url", "name")
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v


class TestCaseAssertsForm(BaseModel):
    id: int = None
    name: str
    case_id: int
    assert_type: str
    expected: str
    actually: str

    @validator("name", "case_id", "assert_type", "expected", "actually")
    def name_not_empty(cls, v):
        return PityModel.not_empty(v)

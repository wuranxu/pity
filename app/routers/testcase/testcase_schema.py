from pydantic import BaseModel, validator

from app.excpetions.ParamsException import ParamsError


class TestCaseForm(BaseModel):
    id: int = None
    catalogue: str
    priority: str
    url: str
    name: str
    tag: str = None
    body: str = None
    request_headers: str = None
    request_method: str = None
    status: int
    project_id: int
    request_type: int

    @validator("catalogue", "priority", "status", "project_id", "request_type", "url", "name")
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
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v

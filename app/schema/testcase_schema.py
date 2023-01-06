from typing import List

from pydantic import BaseModel, validator

from app.exception.error import ParamsError
from app.schema.base import PityModel
from app.schema.constructor import ConstructorForm
from app.schema.request import RequestInfo
from app.schema.testcase_data import PityTestcaseDataForm
from app.schema.testcase_out_parameters import PityTestCaseOutParametersForm


class ListTestCaseForm(BaseModel):
    directory_id: int = None
    name: str = ""
    create_user: str = ""


class DeleteTestCaseDto(BaseModel):
    data: List[int]


class TestCaseForm(BaseModel):
    id: int = None
    priority: str
    url: str = ""
    name: str = ""
    case_type: int = 0
    base_path: str = None
    tag: str = None
    body: str = None
    body_type: int = 0
    request_headers: str = None
    request_method: str = None
    status: int
    out_parameters: List[PityTestCaseOutParametersForm] = []
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
    case_id: int = None
    assert_type: str
    expected: str
    actually: str

    @validator("name", "assert_type", "expected", "actually")
    def name_not_empty(cls, v):
        return PityModel.not_empty(v)


class TestCaseInfo(BaseModel):
    case: TestCaseForm = None
    asserts: List[TestCaseAssertsForm] = []
    data: List[PityTestcaseDataForm] = []
    constructor: List[ConstructorForm] = []
    out_parameters: List[PityTestCaseOutParametersForm] = []

    @validator("case")
    def name_not_empty(cls, v):
        return PityModel.not_empty(v)


class TestCaseGeneratorForm(BaseModel):
    directory_id: int
    requests: List[RequestInfo]
    name: str

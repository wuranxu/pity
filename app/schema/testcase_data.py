from pydantic import BaseModel, validator

from app.schema.base import PityModel


class PityTestcaseDataForm(BaseModel):
    id: int = None
    case_id: int
    name: str
    json_data: str
    env: int

    @validator("case_id", "env", "name", "json_data")
    def name_not_empty(cls, v):
        return PityModel.not_empty(v)

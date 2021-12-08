from pydantic import BaseModel, validator

from app.models.schema.base import PityModel


class PyScriptForm(BaseModel):
    command: str
    value: str

    @validator("command")
    def name_not_empty(cls, v):
        return PityModel.not_empty(v)

from pydantic import BaseModel, validator

from app.schema.base import PityModel


class OnlineSQLForm(BaseModel):
    id: int = None
    sql: str

    @validator("sql", 'id')
    def name_not_empty(cls, v):
        return PityModel.not_empty(v)

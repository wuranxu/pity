from pydantic import BaseModel, validator

from app.schema.base import PityModel


class OnlineRedisForm(BaseModel):
    id: int = None
    command: str

    @validator("command", 'id')
    def name_not_empty(cls, v):
        return PityModel.not_empty(v)

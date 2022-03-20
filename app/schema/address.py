from pydantic import validator, BaseModel

from app.schema.base import PityModel


class Address(BaseModel):
    id: int = None
    env: int = None
    name: str = ''
    gateway: str = ''

    @property
    def parameters(self):
        return [self.env, self.name, self.gateway]

    @validator("env", 'name', 'gateway')
    def name_not_empty(cls, v):
        return PityModel.not_empty(v)

from pydantic import validator, BaseModel

from app.schema.base import PityModel


class PityAddressForm(BaseModel):
    id: int = None
    env: int = None
    name: str = ''
    gateway: str = ''

    @validator("env", 'name', 'gateway')
    def name_not_empty(cls, v):
        return PityModel.not_empty(v)

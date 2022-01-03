from pydantic import BaseModel, validator

# 都可以为空，为空则不进行更改
from app.models.schema.base import PityModel


class UserUpdateForm(BaseModel):
    id: int
    name: str = None
    email: str = None
    phone: str = None
    role: int = None
    is_valid: bool = None

    @validator('id')
    def id_not_empty(cls, v):
        return PityModel.not_empty(v)

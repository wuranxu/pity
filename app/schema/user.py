from pydantic import BaseModel, validator

# 都可以为空，为空则不进行更改
from app.exception.error import ParamsError
from app.schema.base import PityModel


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


class UserDto(BaseModel):
    name: str
    password: str
    username: str
    email: str

    @validator('name', 'password', 'username', 'email')
    def field_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v


class UserForm(BaseModel):
    username: str
    password: str

    @validator('password', 'username')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v


class ResetPwdForm(BaseModel):
    password: str
    token: str

    @validator('token', 'password')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v

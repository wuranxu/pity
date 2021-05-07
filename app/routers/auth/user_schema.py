from pydantic import BaseModel, validator

from app.excpetions.ParamsException import ParamsError


class UserDto(BaseModel):
    name: str
    password: str
    username: str
    email: str

    @validator('name', 'password', 'username', 'email')
    def field_not_empty(cls, v):
        if len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v


class UserForm(BaseModel):
    username: str
    password: str

    @validator('password', 'username')
    def name_not_empty(cls, v):
        if len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v

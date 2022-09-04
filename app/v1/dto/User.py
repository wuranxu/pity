from pydantic import BaseModel, EmailStr


class UserInfo(BaseModel):
    role: int
    name: str
    email: str
    id: int = None


class UserLoginRequest(BaseModel):
    username: str
    password: str


class UserRegisterRequest(BaseModel):
    name: str
    password: str
    username: str
    email: EmailStr


class UserQueryRequest(BaseModel):
    token: str


class GenerateUrlRequest(BaseModel):
    email: EmailStr

from pydantic import BaseModel


# 都可以为空，为空则不进行更改
class UserUpdateForm(BaseModel):
    id: int = None
    name: str = None
    email: str = None
    role: int = None
    is_valid: bool = None

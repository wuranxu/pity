from pydantic import validator, BaseModel

from app.exception.error import ParamsError


class ProjectForm(BaseModel):
    name: str
    app: str
    owner: int
    private: bool = False
    description: str = ''
    dingtalk_url: str = None

    @validator('name', 'app', 'owner')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v


class ProjectEditForm(BaseModel):
    id: int
    name: str
    app: str
    owner: int
    private: bool = False
    description: str = ''
    dingtalk_url: str = None

    @validator('id', 'name', 'app', 'owner')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v


class ProjectRoleForm(BaseModel):
    user_id: int
    project_role: int
    project_id: int

    @validator('user_id', 'project_role', 'project_id')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v


class ProjectRoleEditForm(BaseModel):
    id: int
    user_id: int
    project_role: int
    project_id: int

    @validator('id', 'user_id', 'project_role', 'project_id')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v


class ProjectDelForm(BaseModel):
    id: int

    @validator('id')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v

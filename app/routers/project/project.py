from fastapi import APIRouter, Depends

from app.crud.project.ProjectDao import ProjectDao
from app.crud.project.ProjectRoleDao import ProjectRoleDao
from app.handler.fatcory import PityResponse
from app.routers import Permission
from app.routers.project.project_schema import ProjectForm, ProjectEditForm
from app.routers.project.project_schema import ProjectRoleForm, ProjectRoleEditForm, ProjectDelForm
from config import Config

router = APIRouter(prefix="/project")


@router.get("/list")
async def list_project(page: int = 1, size: int = 8, name: str = "", user_info=Depends(Permission())):
    """
    获取项目列表
    :param name: 项目名称
    :param size:
    :param page:
    :param user_info:
    :return:
    """
    # page, size = PageHandler.page()
    user_role, user_id = user_info["role"], user_info["id"]
    # name = request.args.get("name")
    result, total, err = ProjectDao.list_project(user_id, user_role, page, size, name)
    if err is not None:
        return dict(code=110, data=result, msg=err)
    return dict(code=0, data=PityResponse.model_to_list(result), total=total, msg="操作成功")


@router.post("/insert")
async def insert_project(data: ProjectForm, user_info=Depends(Permission(Config.MANAGER))):
    try:
        err = ProjectDao.add_project(user=user_info["id"], **data.dict())
        if err is not None:
            return dict(code=110, msg=err)
        return dict(code=0, msg="操作成功")
    except Exception as e:
        return dict(code=110, msg=str(e))


@router.post("/update")
async def update_project(data: ProjectEditForm, user_info=Depends(Permission())):
    try:
        user_id, role = user_info["id"], user_info["role"]
        err = ProjectDao.update_project(user=user_id, role=role, **data.dict())
        if err is not None:
            return dict(code=110, msg=err)
        return dict(code=0, msg="操作成功")
    except Exception as e:
        return dict(code=110, msg=str(e))


@router.get("/query")
def query_project(projectId: int, user_info=Depends(Permission())):
    result = dict()
    data, roles, err = ProjectDao.query_project(projectId)
    if err is not None:
        return dict(code=110, data=result, msg=err)
    result.update({"project": PityResponse.model_to_dict(data), "roles": PityResponse.model_to_list(roles)})
    return dict(code=0, data=result, msg="操作成功")


@router.post("/role/insert")
async def insert_project_role(role: ProjectRoleForm, user_info=Depends(Permission())):
    try:
        err = ProjectRoleDao.add_project_role(**role.dict(),
                                              user=user_info["id"], user_role=user_info["role"])
        if err is not None:
            return dict(code=110, msg=err)
    except Exception as e:
        return dict(code=110, msg=str(e))
    return dict(code=0, msg="操作成功")


@router.post("/role/update")
async def update_project_role(role: ProjectRoleEditForm, user_info=Depends(Permission())):
    try:
        err = ProjectRoleDao.update_project_role(role.id, role.project_role,
                                                 user_info["id"], user_info["role"])
        if err is not None:
            return dict(code=110, msg=err)
    except Exception as e:
        return dict(code=110, msg=str(e))
    return dict(code=0, msg="操作成功")


@router.post("/role/delete")
async def delete_project_role(role: ProjectDelForm, user_info=Depends(Permission())):
    try:
        err = ProjectRoleDao.delete_project_role(role.id, user_info["id"], user_info["role"])
        if err is not None:
            return dict(code=110, msg=err)
    except Exception as e:
        return dict(code=110, msg=str(e))
    return dict(code=0, msg="操作成功")

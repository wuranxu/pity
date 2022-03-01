import traceback

from fastapi import APIRouter, Depends, File, UploadFile

from app.crud.project.ProjectDao import ProjectDao
from app.crud.project.ProjectRoleDao import ProjectRoleDao
from app.handler.fatcory import PityResponse
from app.middleware.oss import OssClient
from app.models.project_role import ProjectRole
from app.routers import Permission
from app.routers.project.project_schema import ProjectForm, ProjectEditForm
from app.routers.project.project_schema import ProjectRoleForm, ProjectRoleEditForm, ProjectDelForm
from config import Config

router = APIRouter(prefix="/project")


@router.get("/list")
def list_project(page: int = 1, size: int = 8, name: str = "", user_info=Depends(Permission())):
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
        err = await ProjectDao.add_project(user=user_info["id"], **data.dict())
        if err is not None:
            return dict(code=110, msg=err)
        return dict(code=0, msg="操作成功")
    except Exception as e:
        return dict(code=110, msg=str(e))


@router.post("/avatar/{project_id}")
async def update_project_avatar(project_id: int, file: UploadFile = File(...), user_info=Depends(Permission())):
    try:
        file_content = await file.read()
        suffix = file.filename.split(".")[-1]
        filepath = f"project_{project_id}.{suffix}"
        client = OssClient.get_oss_client()
        file_url, _, _ = await client.create_file(filepath, file_content, base_path="avatar")
        err = await ProjectDao.update_avatar(project_id, user_info['id'], user_info['role'], file_url)
        if err:
            return PityResponse.failed(err)
        return PityResponse.success(file_url)
    except Exception as e:
        return PityResponse.failed(f"上传头像失败: {e}")


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


@router.delete("/delete", description="删除项目")
async def query_project(projectId: int, user_info=Depends(Permission(Config.ADMIN))):
    try:
        await ProjectDao.delete_record_by_id(user_info['id'], projectId)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/role/insert")
async def insert_project_role(role: ProjectRoleForm, user_info=Depends(Permission())):
    try:
        query = await ProjectRoleDao.query_record(user_id=role.user_id, project_id=role.project_id,
                                                  deleted_at=0)
        if query is not None:
            raise Exception("该用户已存在")
        user = user_info['id']
        err = await ProjectRoleDao.has_permission(role.project_id, role.project_role, user, user_info['role'])
        if err is not None:
            raise Exception(err)
        model = ProjectRole(**role.dict(), create_user=user)
        await ProjectRoleDao.insert_record(model, True)
    except Exception as e:
        traceback.print_exc()
        return dict(code=110, msg=str(e))
    return dict(code=0, msg="操作成功")


@router.post("/role/update")
async def update_project_role(role: ProjectRoleEditForm, user_info=Depends(Permission())):
    try:
        await ProjectRoleDao.update_project_role(role, user_info["id"], user_info["role"])
    except Exception as e:
        return dict(code=110, msg=str(e))
    return dict(code=0, msg="操作成功")


@router.post("/role/delete")
async def delete_project_role(role: ProjectDelForm, user_info=Depends(Permission())):
    try:
        await ProjectRoleDao.delete_project_role(role.id, user_info["id"], user_info["role"])
    except Exception as e:
        return dict(code=110, msg=str(e))
    return dict(code=0, msg="操作成功")

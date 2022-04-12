import traceback

from fastapi import APIRouter, Depends, File, UploadFile

from app.crud.project.ProjectDao import ProjectDao
from app.crud.project.ProjectRoleDao import ProjectRoleDao
from app.crud.test_case.TestPlan import PityTestPlanDao
from app.excpetions.AuthException import AuthException
from app.handler.fatcory import PityResponse
from app.middleware.oss import OssClient
from app.models.project_role import ProjectRole
from app.routers import Permission, get_session
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
    user_role, user_id = user_info["role"], user_info["id"]
    result, total, err = ProjectDao.list_project(user_id, user_role, page, size, name)
    if err is not None:
        return PityResponse.failed(code=110, data=result, msg=err)
    return PityResponse.success_with_size(data=result, total=total)


@router.post("/insert")
async def insert_project(data: ProjectForm, user_info=Depends(Permission(Config.MANAGER))):
    try:
        err = await ProjectDao.add_project(user=user_info["id"], **data.dict())
        if err is not None:
            return PityResponse.failed(err)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/avatar/{project_id}", summary="上传项目头像")
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
            return PityResponse.failed(err)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(e)


@router.get("/query")
async def query_project(projectId: int, user_info=Depends(Permission())):
    try:
        result = dict()
        data, roles = await ProjectDao.query_project(projectId)
        await ProjectRoleDao.access(user_info["id"], user_info["role"], roles, data)
        result.update({"project": data, "roles": roles})
        return PityResponse.success(result)
    except AuthException:
        return PityResponse.forbidden()
    except Exception as e:
        return PityResponse.failed(e)


@router.delete("/delete", description="删除项目")
async def query_project(projectId: int, user_info=Depends(Permission(Config.MEMBER)), session=Depends(get_session)):
    try:
        async with session.begin():
            # 事务开始
            owner = await ProjectDao.is_project_admin(session, projectId, user_info["id"])
            if not owner and user_info["role"] != Config.ADMIN:
                return PityResponse.forbidden()
            await ProjectDao.delete_record_by_id(session, user_info['id'], projectId)
            # 有可能项目没有测试计划 2022-03-14 fixed bug
            await PityTestPlanDao.delete_record_by_id(session, user_info['id'], projectId, key="project_id",
                                                      exists=False)
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
        return PityResponse.failed(e)
    return PityResponse.success()


@router.post("/role/update")
async def update_project_role(role: ProjectRoleEditForm, user_info=Depends(Permission())):
    try:
        await ProjectRoleDao.update_project_role(role, user_info["id"], user_info["role"])
    except Exception as e:
        return PityResponse.failed(e)
    return PityResponse.success()


@router.post("/role/delete")
async def delete_project_role(role: ProjectDelForm, user_info=Depends(Permission())):
    try:
        await ProjectRoleDao.delete_project_role(role.id, user_info["id"], user_info["role"])
    except Exception as e:
        return PityResponse.failed(e)
    return PityResponse.success()

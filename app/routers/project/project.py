from fastapi import APIRouter, Depends, File, UploadFile

from app.crud.project.ProjectDao import ProjectDao
from app.crud.project.ProjectRoleDao import ProjectRoleDao
from app.crud.test_case.TestPlan import PityTestPlanDao
from app.exception.error import AuthError
from app.handler.fatcory import PityResponse
from app.middleware.oss import OssClient
from app.models.project_role import ProjectRole
from app.routers import Permission, get_session
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
    user_role, user_id = user_info["role"], user_info["id"]
    result, total = await ProjectDao.list_project(user_id, user_role, page, size, name)
    return PityResponse.success_with_size(data=result, total=total)


@router.post("/insert")
async def insert_project(data: ProjectForm, user_info=Depends(Permission(Config.MANAGER))):
    await ProjectDao.add_project(user_id=user_info["id"], **data.dict())
    return PityResponse.success()


@router.post("/avatar/{project_id}", summary="上传项目头像")
async def update_project_avatar(project_id: int, file: UploadFile = File(...), user_info=Depends(Permission())):
    try:
        file_content = await file.read()
        suffix = file.filename.split(".")[-1]
        filepath = f"project_{project_id}.{suffix}"
        client = OssClient.get_oss_client()
        file_url, _ = await client.create_file(filepath, file_content, base_path="avatar")
        await ProjectDao.update_avatar(project_id, user_info['id'], user_info['role'], file_url)
        return PityResponse.success(file_url)
    except Exception as e:
        return PityResponse.failed(e)


@router.post("/update")
async def update_project(data: ProjectEditForm, user_info=Depends(Permission())):
    user_id, role = user_info["id"], user_info["role"]
    await ProjectDao.update_project(user_id=user_id, role=role, **data.dict())
    return PityResponse.success()


@router.get("/query")
async def query_project(projectId: int, user_info=Depends(Permission())):
    try:
        result = dict()
        data, roles = await ProjectDao.query_project(projectId)
        await ProjectRoleDao.access(user_info["id"], user_info["role"], roles, data)
        result.update({"project": data, "roles": roles})
        return PityResponse.success(result)
    except AuthError:
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
            await ProjectDao.delete_record_by_id(session, user_info['id'], projectId, session_begin=True)
            # 有可能项目没有测试计划 2022-03-14 fixed bug
            await PityTestPlanDao.delete_record_by_id(session, user_info['id'], projectId, key="project_id",
                                                      exists=False, session_begin=True)
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
        await ProjectRoleDao.has_permission(role.project_id, role.project_role, user_info['id'], user_info['role'])
        model = ProjectRole(**role.dict(), create_user=user_info['id'])
        await ProjectRoleDao.insert(model=model, log=True)
    except Exception as e:
        return PityResponse.failed(e)
    return PityResponse.success()


@router.post("/role/update")
async def update_project_role(role: ProjectRoleEditForm, user_info=Depends(Permission())):
    await ProjectRoleDao.update_project_role(role, user_info["id"], user_info["role"])
    return PityResponse.success()


@router.post("/role/delete")
async def delete_project_role(role: ProjectDelForm, user_info=Depends(Permission())):
    await ProjectRoleDao.delete_project_role(role.id, user_info["id"], user_info["role"])
    return PityResponse.success()

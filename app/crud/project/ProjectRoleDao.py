from copy import deepcopy
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import Mapper, ModelWrapper
from app.enums.OperationEnum import OperationType
from app.exception.error import AuthError
from app.models import async_session
from app.models.project import Project
from app.models.project_role import ProjectRole
from app.routers.project.project_schema import ProjectRoleEditForm
from config import Config


# 1. 有同步 也有异步代码（历史问题）
# 2. 变量命名不规范，有的带了类型 有的没带
# 3. 不能只返回List，要带上具体的类型
# 4. 应该多封装自定义异常，这样一下子就能清楚是什么报错


@ModelWrapper(ProjectRole)
class ProjectRoleDao(Mapper):

    @classmethod
    async def list_project_by_user(cls, user_id: int) -> List[int]:
        """
        通过user_id获取项目列表
        :param user_id:
        :return:
        """
        try:
            async with async_session() as session:
                data = await session.execute(
                    select(ProjectRole.project_id).where(ProjectRole.user_id == user_id, ProjectRole.deleted_at == 0))
                return data.scalars().all()
        except Exception as e:
            cls.__log__.error(f"查询用户: {user_id}项目失败, {e}")
            raise Exception("获取项目失败")

    @staticmethod
    async def list_role(project_id: int) -> List[ProjectRole]:
        try:
            async with async_session() as session:
                query = await session.execute(
                    select(ProjectRole).where(ProjectRole.project_id == project_id, ProjectRole.deleted_at == 0))
                return query.scalars().all()
        except Exception as e:
            ProjectRoleDao.__log__.error(f"查询项目: {project_id}角色列表失败, {e}")
            raise Exception(f"获取项目角色列表失败")

    @staticmethod
    async def judge_permission(session: AsyncSession, project_id: int, user_id: int, project_role: int,
                               project_admin: bool) -> None:
        """
        判断用户是否有某个项目的权限
        :param session:
        :param project_id:
        :param user_id:
        :param project_role:
        :param project_admin: 是否是项目管理员
        :return:
        """
        query = await session.execute(select(Project).where(Project.id == project_id))
        project = query.scalars().first()
        if project is None:
            raise Exception("该项目不存在")
        if project.owner != user_id:
            if project_admin and project_role == Config.MANAGER:
                raise Exception("不能修改组长的权限")
            query = await session.execute(select(ProjectRole)
                                          .where(ProjectRole.user_id == user_id,
                                                 ProjectRole.project_id == project_id,
                                                 ProjectRole.deleted_at == 0))
            updater_role = query.scalars().first()
            if updater_role is None or updater_role.project_role == Config.MEMBER:
                raise Exception("对不起，你没有权限")

    @staticmethod
    async def access(user: int, user_role: int, roles: List[ProjectRole], project: Project = None):
        if user_role == Config.ADMIN or not project.private or user == project.owner:
            return
        if not any([r.user_id == user for r in roles]):
            raise AuthError("没有权限访问项目")

    @staticmethod
    async def read_permission(project_id: int, user_id: int, user_role: int):
        """
        判断用户是否有读取项目的权限
        :param user_role:
        :param project_id:
        :param user_id:
        :return:
        """
        if user_role == Config.ADMIN:
            # 超管不需要判断权限
            return
        async with async_session() as session:
            query = await session.execute(select(Project).where(Project.id == project_id, Project.deleted_at == 0))
            project = query.scalars().first()
            if project is None:
                raise Exception("项目不存在")
            if project.private and project.owner != user_id:
                query = await session.execute(select(ProjectRole).where(ProjectRole.user_id == user_id,
                                                                        ProjectRole.project_id == project_id,
                                                                        ProjectRole.deleted_at == 0))
                role = query.scalars().first()
                if role is None:
                    raise AuthError("没有权限访问项目")

    @staticmethod
    async def has_permission(project_id: int, project_role: int, user_id: int, user_role: int,
                             project_admin: bool = False, session: AsyncSession = None):
        """
        判断用户是否有该项目的权限
        :param project_id:
        :param project_role:
        :param user_id:
        :param user_role:
        :param project_admin:
        :param session:
        :return:
        """
        if user_role != Config.ADMIN:
            if session is not None:
                await ProjectRoleDao.judge_permission(session, project_id, user_id, project_role, project_admin)
            async with async_session() as session:
                await ProjectRoleDao.judge_permission(session, project_id, user_id, project_role, project_admin)

    @classmethod
    async def update_project_role(cls, role: ProjectRoleEditForm, user_id: int, user_role: int):
        """
        更改用户角色
        :param role:
        :param user_id:
        :param user_role:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    original = await ProjectRoleDao.query_record(session=session, id=role.id, deleted_at=0)
                    if original is None:
                        raise Exception("该用户角色不存在")
                    await ProjectRoleDao.has_permission(original.project_id, original.project_role, user_id,
                                                        user_role, True, session=session)
                    old = deepcopy(original)
                    changed = ProjectRoleDao.update_model(original, role, user_id)
                    await session.flush()
                    session.expunge(original)
                    await ProjectRoleDao.insert_log(session, user_id, OperationType.UPDATE, original, old, role.id,
                                                    changed=changed)
        except Exception as e:
            cls.__log__.error(f"更新用户角色失败: {e}")
            raise Exception(f"更新用户角色失败: {e}")

    @staticmethod
    async def delete_project_role(role_id: int, user_id: int, user_role: int) -> None:
        """
        删除用户角色
        :param role_id:
        :param user_id:
        :param user_role:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    role = await ProjectRoleDao.query_record(session=session, id=role_id, deleted_at=0)
                    if role is None:
                        raise Exception("用户角色不存在")
                    await ProjectRoleDao.has_permission(role.project_id, role.project_role, user_id, user_role, True,
                                                        session=session)
                    ProjectRoleDao.delete_model(role, user_id)
                    await session.flush()
                    session.expunge(role)
                    await ProjectRoleDao.insert_log(session, user_id, OperationType.DELETE, role, key=role_id)
        except Exception as e:
            raise Exception(f"删除用户角色失败: {e}")

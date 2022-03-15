import asyncio
from copy import deepcopy
from typing import List

from sqlalchemy import select

from app.crud import Mapper
from app.excpetions.AuthException import AuthException
from app.models import Session, async_session, DatabaseHelper
from app.models.project import Project
from app.models.project_role import ProjectRole
from app.routers.project.project_schema import ProjectRoleEditForm
from app.utils.decorator import dao
from app.utils.logger import Log
from config import Config


@dao(ProjectRole, Log("ProjectRoleDao"))
class ProjectRoleDao(Mapper):
    @staticmethod
    def list_project_by_user(user_id) -> (List, str):
        """
        通过user_id获取项目列表
        :param user_id:
        :return:
        """
        try:
            with Session() as session:
                projects = session.query(ProjectRole).filter_by(user_id=user_id, deleted_at=0).all()
                return [p.project_id for p in projects], None
        except Exception as e:
            ProjectRoleDao.log.error(f"查询用户: {user_id}项目失败, {e}")
            return [], f"查询项目失败, {e}"

    @staticmethod
    async def list_role(project_id: int):
        try:
            async with async_session() as session:
                query = await session.execute(
                    select(ProjectRole).where(ProjectRole.project_id == project_id, ProjectRole.deleted_at == 0))
                return query.scalars().all()
        except Exception as e:
            ProjectRoleDao.log.error(f"查询项目: {project_id}角色列表失败, {e}")
            raise Exception(f"获取项目角色列表失败")

    @staticmethod
    async def judge_permission(session, project_id, user, project_role, project_admin):
        query = await session.execute(select(Project).where(Project.id == project_id))
        project = query.scalars().first()
        if project is None:
            return "该项目不存在"
        if project.owner != user:
            if project_admin and project_role == Config.MANAGER:
                return "不能修改组长的权限"
            query = await session.execute(select(ProjectRole)
                                          .where(ProjectRole.user_id == user,
                                                 ProjectRole.project_id == project_id,
                                                 ProjectRole.deleted_at == 0))
            updater_role = query.scalars().first()
            if updater_role is None or updater_role.project_role == Config.MEMBER:
                return "对不起，你没有权限"
        return None

    @staticmethod
    async def access(user: int, user_role: int, roles: List[ProjectRole], project: Project = None):
        if user_role == Config.ADMIN or not project.private or user == project.owner:
            return
        if not any([r.user_id == user for r in roles]):
            raise AuthException("没有权限访问项目")

    @staticmethod
    async def read_permission(project_id: int, user: int, user_role: int):
        """
        判断用户是否有读取项目的权限
        :param user_role:
        :param project_id:
        :param user:
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
            if project.private and project.owner != user:
                query = await session.execute(select(ProjectRole).where(ProjectRole.user_id == user,
                                                                        ProjectRole.project_id == project_id,
                                                                        ProjectRole.deleted_at == 0))
                role = query.scalars().first()
                if role is None:
                    raise AuthException("没有权限访问项目")

    @staticmethod
    async def has_permission(project_id, project_role, user, user_role, project_admin=False, session=None):
        if user_role != Config.ADMIN:
            if session is not None:
                return await ProjectRoleDao.judge_permission(session, project_id, user, project_role, project_admin)
            async with async_session() as session:
                return await ProjectRoleDao.judge_permission(session, project_id, user, project_role, project_admin)
        return None

    # @staticmethod
    # def add_project_role(user_id, project_id, project_role, user, user_role):
    #     """
    #     为项目添加用户
    #     :param user_id: 用户id
    #     :param project_id: 项目id
    #     :param project_role: 用户角色
    #     :param user: 创建人
    #     :param user_role: 创建人角色
    #     :return:
    #     """
    #     try:
    #         with Session() as session:
    #             role = session.query(ProjectRole).filter_by(user_id=user_id, project_id=project_id,
    #                                                         deleted_at=0).first()
    #             if role is not None:
    #                 # 说明角色已经存在了
    #                 return "该用户已存在"
    #             err = ProjectRoleDao.has_permission(project_id, project_role, user, user_role)
    #             if err is not None:
    #                 return err
    #             role = ProjectRole(user_id, project_id, project_role, user)
    #             session.add(role)
    #             session.commit()
    #     except Exception as e:
    #         ProjectRoleDao.log.error(f"添加项目用户失败, {e}")
    #         return f"添加项目用户失败, {e}"
    #     return None

    @staticmethod
    async def update_project_role(role: ProjectRoleEditForm, user, user_role):
        async with async_session() as session:
            async with session.begin():
                original = await ProjectRoleDao.query_record(session=session, id=role.id, deleted_at=0)
                if original is None:
                    raise Exception("该用户角色不存在")
                err = await ProjectRoleDao.has_permission(original.project_id, original.project_role, user,
                                                          user_role, True, session=session)
                if err is not None:
                    raise Exception(err)
                old = deepcopy(original)
                changed = DatabaseHelper.update_model(original, role, user)
                await session.flush()
                session.expunge(original)
            async with session.begin():
                await asyncio.create_task(
                    ProjectRoleDao.insert_log(session, user, Config.OperationType.UPDATE, original, old, role.id,
                                              changed=changed))

    @staticmethod
    async def delete_project_role(role_id, user, user_role):
        async with async_session() as session:
            async with session.begin():
                role = await ProjectRoleDao.query_record(session=session, id=role_id, deleted_at=0)
                if role is None:
                    raise Exception("用户角色不存在")
                err = await ProjectRoleDao.has_permission(role.project_id, role.project_role, user, user_role, True)
                if err is not None:
                    return err
                DatabaseHelper.delete_model(role, user)
                await session.flush()
                session.expunge(role)
            async with session.begin():
                await asyncio.create_task(
                    ProjectRoleDao.insert_log(session, user, Config.OperationType.DELETE, role, key=role_id))

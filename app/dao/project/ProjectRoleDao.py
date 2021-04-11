from datetime import datetime
from typing import List

from app import pity
from app.models import db
from app.models.project import Project
from app.models.project_role import ProjectRole
from app.utils.logger import Log


class ProjectRoleDao(object):
    log = Log("ProjectRoleDao")

    @staticmethod
    def list_project_by_user(user_id) -> (List, str):
        """
        通过user_id获取项目列表
        :param user_id:
        :return:
        """
        try:
            projects = ProjectRole.query.filter_by(user_id=user_id, deleted_at=None).all()
            return [p.id for p in projects], None
        except Exception as e:
            ProjectRoleDao.log.error(f"查询用户: {user_id}项目失败, {e}")
            return [], f"查询项目失败, {e}"

    @staticmethod
    def list_role(project_id: int):
        try:
            roles = ProjectRole.query.filter_by(project_id=project_id, deleted_at=None).all()
            return roles, None
        except Exception as e:
            ProjectRoleDao.log.error(f"查询项目: {project_id}角色列表失败, {e}")
            return [], f"查询项目: {project_id}角色列表失败, {e}"

    @staticmethod
    def add_project_role(user_id, project_id, project_role, user):
        """
        为项目添加用户
        :param user_id: 用户id
        :param project_id: 项目id
        :param project_role: 用户角色
        :param user: 创建人
        :return:
        """
        try:
            role = ProjectRole.query.filter_by(user_id=user_id, project_id=project_id, deleted_at=None).first()
            if role is not None:
                # 说明角色已经存在了
                return "该用户已存在"
            role = ProjectRole(user_id, project_id, project_role, user)
            db.session.add(role)
            db.session.commit()
        except Exception as e:
            ProjectRoleDao.log.error(f"添加项目用户失败, {e}")
            return f"添加项目用户失败, {e}"
        return None

    @staticmethod
    def update_project_role(role_id, project_role, user, user_role):
        try:
            role = ProjectRole.query.filter_by(id=role_id, deleted_at=None).first()
            if role is None:
                return "该用户角色不存在"
            if user_role != pity.config.get("ADMIN"):
                project = Project.query.filter_by(id=role.project_id).first()
                if project is None:
                    return "该项目不存在"
                if project.owner != user and role.project_role == 1:
                    # 说明既不是owner也不是超管，无法修改阻止的权限
                    return "不能修改其他组长的权限"
            updater_role = ProjectRole.query.filter_by(user_id=user, project_id=role.project_id, deleted_at=None).first()
            if updater_role is None or updater_role.project_role == 1:
                return "对不起，你没有权限"
            role.project_role = project_role
            role.updated_at = datetime.now()
            role.update_user = user
            db.session.commit()
        except Exception as e:
            ProjectRoleDao.log.error(f"修改项目用户失败, {e}")
            return f"修改项目用户失败, {e}"
        return None

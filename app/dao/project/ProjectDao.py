from datetime import datetime

from sqlalchemy import or_

from app import pity
from app.dao.project.ProjectRoleDao import ProjectRoleDao
from app.dao.test_case.TestCaseDao import TestCaseDao
from app.models import db
from app.models.project import Project
from app.utils.logger import Log


class ProjectDao(object):
    log = Log("ProjectDao")

    @staticmethod
    def list_project(user, role, page, size, name=None):
        """
        查询/获取项目列表
        :param user: 当前用户
        :param role: 当前用户角色
        :param page: 当前页码
        :param size: 当前size
        :param name: 项目名称
        :return:
        """
        try:
            search = [Project.deleted_at == None]
            if role != pity.config.get("ADMIN"):
                project_list, err = ProjectRoleDao.list_project_by_user(user)
                if err is not None:
                    raise err
                search.append(or_(Project.id in project_list, Project.owner == user, Project.private == False))
            if name:
                search.append(Project.name.ilike("%{}%".format(name)))
            data = Project.query.filter(*search)
            total = data.count()
            return data.order_by(Project.created_at.desc()).paginate(page, per_page=size).items, total, None
        except Exception as e:
            ProjectDao.log.error(f"获取用户: {user}项目列表失败, {e}")
            return [], 0, f"获取用户: {user}项目列表失败, {e}"

    @staticmethod
    def add_project(name, owner, user, private, description):
        try:
            data = Project.query.filter_by(name=name, deleted_at=None).first()
            if data is not None:
                return "项目已存在"
            pr = Project(name, owner, user, description, private)
            db.session.add(pr)
            db.session.commit()
        except Exception as e:
            ProjectDao.log.error(f"新增项目: {name}失败, {e}")
            return f"新增项目: {name}失败, {e}"
        return None

    @staticmethod
    def update_project(user, role, project_id, name, owner, private, description):
        try:
            data = Project.query.filter_by(id=project_id, deleted_at=None).first()
            if data is None:
                return "项目不存在"
            data.name = name
            # 如果修改人不是owner或者超管
            if data.owner != owner and (role < pity.config.get("ADMIN") or user != data.owner):
                return "您没有权限修改项目负责人"
            data.owner = owner
            data.private = private
            data.description = description
            data.updated_at = datetime.now()
            data.update_user = user
            db.session.commit()
        except Exception as e:
            ProjectDao.log.error(f"编辑项目: {name}失败, {e}")
            return f"编辑项目: {name}失败, {e}"
        return None

    @staticmethod
    def query_project(project_id: int):
        try:
            data = Project.query.filter_by(id=project_id, deleted_at=None).first()
            if data is None:
                return None, [], [], "项目不存在"
            roles, err = ProjectRoleDao.list_role(project_id)
            if err is not None:
                return None, [], [], err
            tree, err = TestCaseDao.list_test_case(project_id)
            if err is not None:
                return None, [], [], err
            return data, roles, tree, None
        except Exception as e:
            ProjectDao.log.error(f"查询项目: {project_id}失败, {e}")
            return None, [], [], f"查询项目: {project_id}失败, {e}"

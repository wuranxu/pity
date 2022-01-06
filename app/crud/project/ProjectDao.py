from datetime import datetime

from sqlalchemy import or_, desc, select

from app.crud.project.ProjectRoleDao import ProjectRoleDao
from app.models import Session, async_session
from app.models.project import Project
from app.utils.logger import Log
from config import Config


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
            search = [Project.deleted_at == 0]
            with Session() as session:
                if role != Config.ADMIN:
                    project_list, err = ProjectRoleDao.list_project_by_user(user)
                    if err is not None:
                        raise err
                    search.append(or_(Project.id in project_list, Project.owner == user, Project.private == False))
                if name:
                    search.append(Project.name.ilike("%{}%".format(name)))
                data = session.query(Project).filter(*search)
                total = data.count()
                return data.order_by(desc(Project.created_at)).offset((page - 1) * size).limit(size).all(), total, None
        except Exception as e:
            ProjectDao.log.error(f"获取用户: {user}项目列表失败, {e}")
            return [], 0, f"获取用户: {user}项目列表失败, {e}"

    @staticmethod
    async def add_project(name, app, owner, user, private, description):
        try:
            async with async_session() as session:
                async with session.begin():
                    data = await session.execute(select(Project).where(Project.name == name, Project.deleted_at == 0))
                    if data.scalars().first() is not None:
                        return "项目已存在"
                    pr = Project(name, app, owner, user, description, private)
                    session.add(pr)
        except Exception as e:
            ProjectDao.log.error(f"新增项目: {name}失败, {e}")
            return f"新增项目: {name}失败, {e}"
        return None

    @staticmethod
    async def update_avatar(project_id: int, user_id: int, user_role: int, file_url: str):
        try:
            async with async_session() as session:
                async with session.begin():
                    query = await session.execute(
                        select(Project).where(Project.id == project_id, Project.deleted_at == 0))
                    data = query.scalars().first()
                    if data is None:
                        return "项目不存在"
                    if data.owner != user_id and user_role < Config.ADMIN:
                        return "您没有权限修改项目头像"
                    # 如果修改人不是owner或者超管
                    data.avatar = file_url
                    data.updated_at = datetime.now()
                    data.update_user = user_id
        except Exception as e:
            ProjectDao.log.error(f"修改项目头像失败, 项目: {project_id}, error: {e}")
            return "修改头像失败"
        return None

    @staticmethod
    def update_project(id, user, role, name, app, owner, private, description):
        try:
            with Session() as session:
                data = session.query(Project).filter_by(id=id, deleted_at=0).first()
                if data is None:
                    return "项目不存在"
                data.name = name
                data.app = app
                # 如果修改人不是owner或者超管
                if data.owner != owner and role < Config.ADMIN and user != data.owner:
                    return "您没有权限修改项目负责人"
                data.owner = owner
                data.private = private
                data.description = description
                data.updated_at = datetime.now()
                data.update_user = user
                session.commit()
        except Exception as e:
            ProjectDao.log.error(f"编辑项目: {name}失败, {e}")
            return f"编辑项目: {name}失败, {e}"
        return None

    @staticmethod
    def query_project(project_id: int):
        try:
            with Session() as session:
                data = session.query(Project).filter_by(id=project_id, deleted_at=0).first()
                if data is None:
                    return None, [], "项目不存在"
                roles, err = ProjectRoleDao.list_role(project_id)
                if err is not None:
                    return None, [], err
                # tree, err = TestCaseDao.list_test_case(project_id)
                # if err is not None:
                #     return None, [], [], err
                return data, roles, None
        except Exception as e:
            ProjectDao.log.error(f"查询项目: {project_id}失败, {e}")
            return None, [], f"查询项目: {project_id}失败, {e}"

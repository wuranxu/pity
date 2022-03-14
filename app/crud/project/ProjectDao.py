from datetime import datetime

from sqlalchemy import or_, desc, select

from app.crud import Mapper
from app.crud.project.ProjectRoleDao import ProjectRoleDao
from app.models import Session, async_session
from app.models.project import Project
from app.models.project_role import ProjectRole
from app.utils.decorator import dao
from app.utils.logger import Log
from config import Config


@dao(Project, Log("ProjectDao"))
class ProjectDao(Mapper):

    @classmethod
    def list_project(cls, user, role, page, size, name=None):
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
                    # 找出用户能看到的公开项目
                    search.append(or_(Project.id in project_list, Project.owner == user, Project.private == False))
                if name:
                    search.append(Project.name.ilike("%{}%".format(name)))
                data = session.query(Project).filter(*search)
                total = data.count()
                return data.order_by(desc(Project.created_at)).offset((page - 1) * size).limit(size).all(), total, None
        except Exception as e:
            cls.log.error(f"获取用户: {user}项目列表失败, {e}")
            return [], 0, f"获取用户: {user}项目列表失败, {e}"

    @classmethod
    async def list_project_id_by_user(cls, session, user, role):
        """
        获取用户可见的项目
        :return:
        """
        if role == Config.ADMIN:
            return []
        ans = set()
        # 找到包含用户的角色
        roles = await session.execute(select(ProjectRole.project_id).where(ProjectRole.user_id == user,
                                                                           ProjectRole.deleted_at == 0))
        for r in roles.all():
            ans.add(r[0])
        # 找到未删除的项目
        roles = await session.execute(select(Project.id).where(
            or_(Project.private == False, Project.owner == user), Project.deleted_at == 0))
        for r in roles.all():
            ans.add(r[0])
        return list(ans) if len(ans) > 0 else None

    @classmethod
    async def is_project_admin(cls, session, project_id: int, user_id: int):
        query = await session.execute(select(Project.owner).where(Project.id == project_id))
        return query.scalars().first() == user_id

    @classmethod
    async def add_project(cls, name, app, owner, user, private, description, dingtalk_url=''):
        try:
            async with async_session() as session:
                async with session.begin():
                    data = await session.execute(select(Project).where(Project.name == name, Project.deleted_at == 0))
                    if data.scalars().first() is not None:
                        return "项目已存在"
                    pr = Project(name, app, owner, user, description, private, dingtalk_url)
                    session.add(pr)
        except Exception as e:
            cls.log.error(f"新增项目: {name}失败, {e}")
            return f"新增项目: {name}失败, {e}"
        return None

    @classmethod
    async def update_avatar(cls, project_id: int, user_id: int, user_role: int, file_url: str):
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
            cls.log.error(f"修改项目头像失败, 项目: {project_id}, error: {e}")
            return "修改头像失败"
        return None

    @classmethod
    def update_project(cls, id, user, role, name, app, owner, private, description, dingtalk_url=''):
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
                data.dingtalk_url = dingtalk_url
                session.commit()
        except Exception as e:
            cls.log.error(f"编辑项目: {name}失败, {e}")
            return f"编辑项目: {name}失败, {e}"
        return None

    @classmethod
    def query_project(cls, project_id: int):
        try:
            with Session() as session:
                data = session.query(Project).filter_by(id=project_id, deleted_at=0).first()
                if data is None:
                    raise Exception("项目不存在")
                roles, err = ProjectRoleDao.list_role(project_id)
                if err is not None:
                    raise err
                return data, roles
        except Exception as e:
            cls.log.error(f"查询项目: {project_id}失败, {e}")
            raise Exception(f"查询项目: {project_id}失败, {e}")

    @staticmethod
    async def query_user_project(user_id: int) -> int:
        """
        created by woody at 2022-02-13 12:05
        查询用户有多少项目
        :param user_id: 用户id
        :return: 返回项目数量
        """
        ans = set()
        async with async_session() as session:
            async with session.begin():
                # 先选出未被删除的用户
                project_sql = select(Project).where(Project.deleted_at == 0)
                projects = await session.execute(project_sql)
                project_list = []
                # 将数据放入列表，把owner等于该用户的放入列表
                for r in projects.scalars().all():
                    project_list.append(r.id)
                    if r.owner == user_id:
                        ans.add(r.id)
                # 接着查询项目角色表有该用户的角色，把角色的项目id放入列表
                # 由于是set，所以不会重复
                query = await session.execute(
                    select(ProjectRole).where(ProjectRole.deleted_at == 0, ProjectRole.user_id == user_id))
                for q in query.scalars().all():
                    ans.add(q.project_id)
        return len(ans)

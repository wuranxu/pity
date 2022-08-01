from datetime import datetime
from typing import List

from sqlalchemy import or_, select, desc

from app.crud import Mapper, ModelWrapper
from app.crud.project.ProjectRoleDao import ProjectRoleDao
from app.models import async_session
from app.models.project import Project
from app.models.project_role import ProjectRole
from config import Config


@ModelWrapper(Project)
class ProjectDao(Mapper):

    @classmethod
    async def list_project(cls, user_id: int, role: int, page: int,
                           size: int, name: str = None) -> (List[Project], int):
        """
        查询/获取项目列表
        :param user_id: 当前用户
        :param role: 当前用户角色
        :param page: 当前页码
        :param size: 当前size
        :param name: 项目名称
        :return: 项目列表和总数
        """
        try:
            search = [Project.deleted_at == 0]
            async with async_session() as session:
                if role != Config.ADMIN:
                    project_list = await ProjectRoleDao.list_project_by_user(user_id)
                    # 找出用户能看到的公开项目
                    search.append(or_(Project.id.in_(project_list), Project.owner == user_id, Project.private == False))
                if name:
                    search.append(Project.name.like("%{}%".format(name)))
                sql = select(Project).where(*search).order_by(desc(Project.updated_at))
                data = await session.execute(sql)
                sql = sql.offset((page - 1) * size).limit(size)
                total = data.raw.rowcount
                data = await session.execute(sql)
                return data.scalars().all(), total
        except Exception as e:
            cls.__log__.error(f"获取用户: {user_id}项目列表失败, {e}")
            raise Exception(f"获取用户: {user_id}项目列表失败")

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
    async def add_project(cls, name, app, owner, user_id, private, description, dingtalk_url=''):
        try:
            async with async_session() as session:
                async with session.begin():
                    data = await session.execute(select(Project).where(Project.name == name, Project.deleted_at == 0))
                    if data.scalars().first() is not None:
                        raise Exception("项目已存在")
                    pr = Project(name, app, owner, user_id, description, private, dingtalk_url)
                    session.add(pr)
        except Exception as e:
            cls.__log__.error(f"新增项目: {name}失败, {e}")
            raise Exception(f"新增项目: {name}失败, {e}")

    @classmethod
    async def update_avatar(cls, project_id: int, user_id: int, user_role: int, file_url: str):
        try:
            async with async_session() as session:
                async with session.begin():
                    query = await session.execute(
                        select(Project).where(Project.id == project_id, Project.deleted_at == 0))
                    data = query.scalars().first()
                    if data is None:
                        raise Exception("项目不存在")
                    if data.owner != user_id and user_role < Config.ADMIN:
                        raise Exception("你没有权限修改项目头像")
                    # 如果修改人不是owner或者超管
                    data.avatar = file_url
                    data.updated_at = datetime.now()
                    data.update_user = user_id
        except Exception as e:
            cls.__log__.error(f"修改项目头像失败, 项目: {project_id}, error: {e}")
            raise Exception(e)

    @classmethod
    async def update_project(cls, id: int, user_id, role: int, name: str, app: str, owner: int, private: bool,
                             description: str, dingtalk_url: str = '') -> None:
        """
        修改项目
        :param id:
        :param user_id: 修改人
        :param role: 修改者角色
        :param name:
        :param app:
        :param owner:
        :param private:
        :param description:
        :param dingtalk_url:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    query = await session.execute(select(Project).where(Project.id == id, Project.deleted_at == 0))
                    data = query.scalars().first()
                    if data is None:
                        raise Exception("项目不存在")
                    data.name = name
                    data.app = app
                    # 如果修改人不是owner或者超管
                    if data.owner != owner and role < Config.ADMIN and user_id != data.owner:
                        raise Exception("您没有权限修改项目负责人")
                    data.owner = owner
                    data.private = private
                    data.description = description
                    data.updated_at = datetime.now()
                    data.update_user = user_id
                    data.dingtalk_url = dingtalk_url
        except Exception as e:
            cls.__log__.error(f"编辑项目: {name}失败, {e}")
            raise Exception(f"编辑项目: {name}失败, {e}")

    @classmethod
    async def query_project(cls, project_id: int) -> (List[Project], List[ProjectRole]):
        try:
            async with async_session() as session:
                query = await session.execute(select(Project).where(Project.id == project_id, Project.deleted_at == 0))
                data = query.scalars().first()
                if data is None:
                    raise Exception("项目不存在")
                roles = await ProjectRoleDao.list_role(project_id)
                return data, roles
        except Exception as e:
            cls.__log__.error(f"查询项目: {project_id}失败, {e}")
            raise Exception(f"查询项目: {project_id}失败, {e}")

    @staticmethod
    async def query_user_project(user_id: int) -> int:
        """
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

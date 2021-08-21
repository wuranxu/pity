from datetime import datetime

from sqlalchemy import select

from app.models import async_session, DatabaseHelper, db_helper
from app.models.database import PityDatabase
from app.models.schema.database import DatabaseForm
from app.utils.logger import Log


class DbConfigDao(object):
    log = Log("DbConfigDao")

    @staticmethod
    async def list_database(name: str = '', database: str = '', env: int = None):
        """
        通过name, database, env获取数据库配置列表
        :param name: 数据库名称
        :param database: 数据库名
        :param env: 环境
        :return:
        """
        try:
            async with async_session() as session:
                query = [PityDatabase.deleted_at == None]
                if name:
                    query.append(PityDatabase.name.like(f'%{name}%'))
                if database:
                    query.append(PityDatabase.database.like(f"%{database}%"))
                if env is not None:
                    query.append(PityDatabase.env == env)
                result = await session.execute(select(PityDatabase).where(*query))
                return result.scalars().all()
        except Exception as e:
            DbConfigDao.log.error(f"获取数据库配置失败, error: {e}")
            raise Exception("获取数据库配置失败")

    @staticmethod
    async def insert_database(data: DatabaseForm, user: str):
        try:
            async with async_session() as session:
                async with session.begin():
                    result = await session.execute(
                        select(PityDatabase).where(PityDatabase.name == data.name, PityDatabase.deleted_at == None,
                                                   PityDatabase.env == data.env))
                    query = result.scalars().first()
                    if query is not None:
                        raise Exception("数据库配置已存在")
                    session.add(PityDatabase(**data.dict(), user=user))
        except Exception as e:
            DbConfigDao.log.error(f"新增数据库配置: {data.name}失败, {e}")
            raise Exception("新增数据库配置失败")

    @staticmethod
    async def update_database(data: DatabaseForm, user: str):
        try:
            async with async_session() as session:
                async with session.begin():
                    result = await session.execute(select(PityDatabase).where(data.id == PityDatabase.id))
                    query = result.scalars().first()
                    if query is None:
                        raise Exception("数据库配置不存在")
                    db_helper.remove_connection(query.host, query.port, query.username, query.password, query.database)
                    DatabaseHelper.update_model(query, data, user)
        except Exception as e:
            DbConfigDao.log.error(f"编辑数据库配置: {data.name}失败, {e}")
            raise Exception("编辑数据库配置失败")

    @staticmethod
    async def delete_database(id: int, user: str):
        try:
            async with async_session() as session:
                async with session.begin():
                    result = await session.execute(
                        select(PityDatabase).where(id == PityDatabase.id, PityDatabase.deleted_at == None))
                    query = result.scalars().first()
                    if query is None:
                        raise Exception("数据库配置不存在或已删除")
                    query.deleted_at = datetime.now()
                    query.update_user = user
        except Exception as e:
            DbConfigDao.log.error(f"删除数据库配置: {id}失败, {e}")
            raise Exception("删除数据库配置失败")

    @staticmethod
    async def query_database(id: int):
        try:
            async with async_session() as session:
                result = await session.execute(
                    select(PityDatabase).where(PityDatabase.id == id, PityDatabase.deleted_at == None))
                return result.scalars().first()
        except Exception as e:
            DbConfigDao.log.error(f"获取数据库配置失败, error: {e}")
            raise Exception("获取数据库配置失败")

    @staticmethod
    async def online_sql(id: int, sql: str):
        try:
            query = await DbConfigDao.query_database(id)
            if query is None:
                raise Exception("未找到对应的数据库配置")
            data = db_helper.get_connection(query.sql_type, query.host, query.port, query.username, query.password,
                                            query.database)
            session = data.get("session")
            with session() as s:
                result = s.execute(sql)
                data = result.mappings().all()
                return data
        except Exception as e:
            DbConfigDao.log.error(f"查询数据库配置失败, error: {e}")
            raise e

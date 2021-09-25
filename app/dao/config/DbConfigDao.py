import json
from collections import defaultdict
from datetime import datetime
from typing import List

from sqlalchemy import select, MetaData
from sqlalchemy.exc import ResourceClosedError

from app.dao.config.EnvironmentDao import EnvironmentDao
from app.handler.fatcory import PityResponse
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
    async def query_database_by_env_and_name(env: int, name: str):
        try:
            async with async_session() as session:
                result = await session.execute(
                    select(PityDatabase).where(PityDatabase.env == env, PityDatabase.name == name,
                                               PityDatabase.deleted_at == None))
                return result.scalars().first()
        except Exception as e:
            DbConfigDao.log.error(f"获取数据库配置失败, error: {e}")
            raise Exception("获取数据库配置失败")

    @staticmethod
    async def query_database_and_tables():
        """
        方法会查询所有数据库表配置的信息
        :return:
        """
        try:
            # 返回树图, 最外层是环境
            result = []
            env_index = dict()
            env_data, _, _ = EnvironmentDao.list_env(1, 1, exactly=True)
            env_map = {env.id: env.name for env in env_data}
            # 获取数据库相关的信息
            table_map = defaultdict(set)
            async with async_session() as session:
                query = await session.execute(select(PityDatabase).where(PityDatabase.deleted_at == None))
                data = query.scalars().all()
                for d in data:
                    name = env_map[d.env]
                    idx = env_index.get(name)
                    if idx is None:
                        result.append(dict(title=name, key=f"env_{name}", children=list()))
                        idx = len(result) - 1
                        env_index[name] = idx
                    DbConfigDao.get_tables(table_map, d, result[idx]['children'])
                return result, table_map
        except Exception as err:
            DbConfigDao.log.error(f"获取数据库配置详情失败, error: {err}")
            raise Exception(f"获取数据库配置详情失败: {err}")

    @staticmethod
    def get_tables(table_map: dict, data: PityDatabase, children: List):
        conn = db_helper.get_connection(data.sql_type, data.host, data.port, data.username, data.password,
                                        data.database)
        database_child = list()
        dbs = dict(title=f"{data.database}（{data.host}:{data.port}）", key=f"database_{data.id}",
                   children=database_child, sql_type=data.sql_type)
        eng = conn.get('engine')
        meta = MetaData()
        meta.reflect(bind=eng)
        for t in meta.sorted_tables:
            table_map[data.id].add(str(t))
            temp = []
            database_child.append(dict(title=str(t), key=f"table_{data.id}_{t}", children=temp))
            for k, v in t.c.items():
                table_map[data.id].add(k)
                temp.append(dict(
                    title=k,
                    primary_key=v.primary_key,
                    type={str(v.type)},
                    key=f"column_{t}_{data.id}_{k}",
                ))
        children.append(dbs)

    @staticmethod
    async def online_sql(id: int, sql: str):
        try:
            query = await DbConfigDao.query_database(id)
            if query is None:
                raise Exception("未找到对应的数据库配置")
            data = db_helper.get_connection(query.sql_type, query.host, query.port, query.username, query.password,
                                            query.database)
            return await DbConfigDao.execute(data, sql)
        except Exception as e:
            DbConfigDao.log.error(f"查询数据库配置失败, error: {e}")
            raise Exception(f"执行SQL失败: {e}")

    @staticmethod
    async def execute(conn, sql):
        row_count = 0
        try:
            session = conn.get("session")
            with session() as s:
                result = s.execute(sql)
                row_count = result.rowcount
                ans = result.mappings().all()
                return ans
        except ResourceClosedError:
            # 说明是update或其他语句
            return [{"rowCount": row_count}]
        except Exception as e:
            DbConfigDao.log.error(f"查询数据库配置失败, error: {e}")
            raise e

    @staticmethod
    async def execute_sql(env: int, name: str, sql: str):
        try:
            query = await DbConfigDao.query_database_by_env_and_name(env, name)
            if query is None:
                raise Exception("未找到对应的数据库配置")
            data = db_helper.get_connection(query.sql_type, query.host, query.port, query.username, query.password,
                                            query.database)
            result = await DbConfigDao.execute(data, sql)
            _, result = PityResponse.parse_sql_result(result)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            DbConfigDao.log.error(f"查询数据库配置失败, error: {e}")
            raise Exception(f"执行SQL失败: {e}")

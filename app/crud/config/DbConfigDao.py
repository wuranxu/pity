import json
import time

from sqlalchemy import select, MetaData, text
from sqlalchemy.exc import ResourceClosedError

from app.crud import Mapper, ModelWrapper
from app.crud.config.EnvironmentDao import EnvironmentDao
from app.handler.encoder import JsonEncoder
from app.handler.fatcory import PityResponse
from app.middleware.RedisManager import RedisHelper
from app.models import async_session, db_helper
from app.models.database import PityDatabase
from app.models.sql_log import PitySQLHistory
from app.schema.database import DatabaseForm
from app.utils.logger import Log


class DbConfigDao(Mapper):
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
                query = [PityDatabase.deleted_at == 0]
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
    @RedisHelper.up_cache("database:cache")
    async def insert_database(data: DatabaseForm, user: str):
        try:
            async with async_session() as session:
                async with session.begin():
                    result = await session.execute(
                        select(PityDatabase).where(PityDatabase.name == data.name, PityDatabase.deleted_at == 0,
                                                   PityDatabase.env == data.env))
                    query = result.scalars().first()
                    if query is not None:
                        raise Exception("数据库配置已存在")
                    session.add(PityDatabase(**data.dict(), user=user))
        except Exception as e:
            DbConfigDao.log.error(f"新增数据库配置: {data.name}失败, {e}")
            raise Exception("新增数据库配置失败")

    @staticmethod
    @RedisHelper.up_cache("database:cache")
    async def update_database(data: DatabaseForm, user: str):
        try:
            async with async_session() as session:
                async with session.begin():
                    result = await session.execute(select(PityDatabase).where(data.id == PityDatabase.id))
                    query = result.scalars().first()
                    if query is None:
                        raise Exception("数据库配置不存在")
                    db_helper.remove_connection(query.host, query.port, query.username, query.password, query.database)
                    DbConfigDao.update_model(query, data, user)
        except Exception as e:
            DbConfigDao.log.error(f"编辑数据库配置: {data.name}失败, {e}")
            raise Exception("编辑数据库配置失败")

    @staticmethod
    @RedisHelper.up_cache("database:cache")
    async def delete_database(id: int, user: str):
        try:
            async with async_session() as session:
                async with session.begin():
                    result = await session.execute(
                        select(PityDatabase).where(id == PityDatabase.id, PityDatabase.deleted_at == 0))
                    query = result.scalars().first()
                    if query is None:
                        raise Exception("数据库配置不存在或已删除")
                    query.deleted_at = int(time.time() * 1000)
                    query.update_user = user
        except Exception as e:
            DbConfigDao.log.error(f"删除数据库配置: {id}失败, {e}")
            raise Exception("删除数据库配置失败")

    @staticmethod
    async def query_database(id: int):
        try:
            async with async_session() as session:
                result = await session.execute(
                    select(PityDatabase).where(PityDatabase.id == id, PityDatabase.deleted_at == 0))
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
                                               PityDatabase.deleted_at == 0))
                return result.scalars().first()
        except Exception as e:
            DbConfigDao.log.error(f"获取数据库配置失败, error: {e}")
            raise Exception("获取数据库配置失败")

    @staticmethod
    @RedisHelper.cache("database:cache", expired_time=3600 * 3)
    async def query_database_tree():
        """
        方法会查询所有数据库表配置的信息, 不包括表信息
        :return:
        """
        try:
            # 返回树图, 最外层是环境
            result = []
            env_index = dict()
            env_data, _ = await EnvironmentDao.list_env(1, 1, exactly=True)
            env_map = {env.id: env.name for env in env_data}
            # 获取数据库相关的信息
            async with async_session() as session:
                query = await session.execute(select(PityDatabase).where(PityDatabase.deleted_at == 0))
                data = query.scalars().all()
                for d in data:
                    name = env_map[d.env]
                    idx = env_index.get(name)
                    if idx is None:
                        result.append(dict(title=name, key=f"env_{name}", children=list()))
                        idx = len(result) - 1
                        env_index[name] = idx
                    result[env_index[name]]['children'].append(
                        dict(title=f"{d.database}（{d.host}:{d.port}）", key=f"database_{d.id}",
                             children=list(), sql_type=d.sql_type, data=d)
                    )
                return result
        except Exception as err:
            DbConfigDao.log.error(f"获取数据库配置详情失败, error: {err}")
            raise Exception(f"获取数据库配置详情失败: {err}")

    @staticmethod
    @RedisHelper.cache("database:table:cache", expired_time=1800)
    async def get_tables(data: DatabaseForm):
        conn = await db_helper.get_connection(data.sql_type, data.host, data.port, data.username, data.password,
                                              data.database)
        database_child = list()
        eng = conn.get('engine')
        table_set = set()
        async with eng.connect() as conn:
            await conn.run_sync(DbConfigDao.load_table, table_set, data, database_child)
        return database_child, table_set

    @staticmethod
    def load_table(conn, table_map, data, database_child):
        """
        异步加载table及字段
        :param conn:
        :param table_map:
        :param data:
        :param database_child:
        :return:
        """
        meta = MetaData(bind=conn)
        meta.reflect()
        for t in meta.sorted_tables:
            table_map.add(str(t))
            temp = []
            database_child.append(dict(title=str(t), key=f"table_{data.id}_{t}", children=temp))
            for k, v in t.c.items():
                table_map.add(k)
                temp.append(dict(
                    title=k,
                    primary_key=v.primary_key,
                    type={str(v.type)},
                    isLeaf=True,
                    key=f"column_{t}_{data.id}_{k}",
                ))

    @staticmethod
    async def online_sql(id: int, sql: str):
        try:
            query = await DbConfigDao.query_database(id)
            if query is None:
                raise Exception("未找到对应的数据库配置")
            data = await db_helper.get_connection(query.sql_type, query.host, query.port, query.username,
                                                  query.password, query.database)
            return await DbConfigDao.execute(data, sql)
        except Exception as e:
            DbConfigDao.log.error(f"查询数据库配置失败, error: {e}")
            raise Exception(f"执行SQL失败: {e}")

    @staticmethod
    async def execute(conn, sql):
        row_count = 0
        session = conn.get("session")
        async with session() as s:
            async with s.begin():
                try:
                    start = time.perf_counter()
                    result = await s.execute(text(sql))
                    cost = time.perf_counter() - start
                    row_count = result.rowcount
                    ans = result.mappings().all()
                    return ans, int(cost * 1000)
                except ResourceClosedError:
                    # 说明是update或其他语句
                    return [{"rowCount": row_count}]
                except Exception as e:
                    DbConfigDao.log.error(f"查询数据库配置失败, error: {e}")
                    raise Exception(f"执行sql失败: {e}")

    @staticmethod
    async def execute_sql(env: int, name: str, sql: str):
        try:
            query = await DbConfigDao.query_database_by_env_and_name(env, name)
            if query is None:
                raise Exception("未找到对应的数据库配置")
            data = await db_helper.get_connection(query.sql_type, query.host, query.port, query.username,
                                                  query.password,
                                                  query.database)
            result, _ = await DbConfigDao.execute(data, sql)
            _, result = PityResponse.parse_sql_result(result)
            return json.dumps(result, cls=JsonEncoder, ensure_ascii=False)
        except Exception as e:
            DbConfigDao.log.error(f"查询数据库配置失败, error: {e}")
            raise Exception(f"执行SQL失败: {e}")


@ModelWrapper(PitySQLHistory)
class PitySQLHistoryDao(Mapper):
    pass

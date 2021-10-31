import time
from datetime import datetime
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config

# 同步engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_recycle=1500)
# 异步engine
async_engine = create_async_engine(Config.ASYNC_SQLALCHEMY_URI, pool_recycle=1500)

Session = sessionmaker(engine)

async_session = sessionmaker(async_engine, class_=AsyncSession)

# 创建对象的基类:
Base = declarative_base()

Base.metadata.create_all(engine)


class DatabaseHelper(object):

    def __init__(self):
        # cache
        self.connections = dict()

    def get_connection(self, sql_type: int, host: str, port: int, username: str, password: str, database: str):
        # 拼接key
        key = f"{host}:{port}:{database}:{username}:{password}:{database}"
        connection = self.connections.get(key)
        # 先判断是否已经有connection了，如果有则直接返回
        if connection is not None:
            return connection
        # 获取sqlalchemy需要的jdbc url
        jdbc_url = DatabaseHelper.get_jdbc_url(sql_type, host, port, username, password, database)
        if jdbc_url is None:
            return None
        # 创建异步引擎
        eg = create_engine(jdbc_url, pool_recycle=1500)
        # 拿到session方法
        ss = sessionmaker(bind=eg, autocommit=True)
        # 将数据缓存起来
        data = dict(engine=eg, session=ss)
        self.connections[key] = data
        return data

    @staticmethod
    def test_connection(ss):
        if ss is None:
            return "暂不支持的数据库类型"
        try:
            with ss() as session:
                with session.begin():
                    session.execute("select 1")
        except Exception as e:
            return str(e)
        return None

    @staticmethod
    def get_jdbc_url(sql_type: int, host: str, port: int, username: str, password: str, database: str):
        if sql_type == 0:
            # mysql模式
            return f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'
        elif sql_type == 1:
            return f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
        return None

    def remove_connection(self, host: str, port: int, username: str, password: str, database: str):
        key = f"{host}:{port}:{database}:{username}:{password}:{database}"
        if self.connections.get(key):
            self.connections.pop(key)

    @staticmethod
    def update_model(dist, source, update_user=None, not_null=False):
        """
        :param dist:
        :param source:
        :param not_null:
        :param update_user:
        :return:
        """
        for var, value in vars(source).items():
            if not_null:
                if value:
                    setattr(dist, var, value)
            else:
                setattr(dist, var, value)
            if update_user:
                setattr(dist, 'update_user', update_user)
            setattr(dist, 'updated_at', datetime.now())

    @staticmethod
    def delete_model(dist, update_user):
        """
        删除数据，兼容老的deleted_at
        :param dist:
        :param update_user:
        :return:
        """
        if str(dist.__class__.deleted_at.property.columns[0].type) == "DATETIME":
            dist.deleted_at = datetime.now()
        else:
            dist.deleted_at = time.time()
        dist.updated_at = datetime.now()
        dist.update_user = update_user

    @classmethod
    def where(cls, param, sentence, condition: List):
        if param:
            condition.append(sentence)
        return cls

    @staticmethod
    async def pagination(page: int, size: int, session, sql):
        """
        分页查询
        :param session:
        :param page:
        :param size:
        :param sql:
        :return:
        """
        data = await session.execute(sql)
        total = data.raw.rowcount
        if total == 0:
            return [], 0
        sql = sql.offset((page - 1) * size).limit(size)
        data = await session.execute(sql)
        return data.scalars().all(), total


db_helper = DatabaseHelper()

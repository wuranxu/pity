import importlib
import os
import sys

from sqlalchemy import select

from app.models import Base, engine, async_session, DatabaseHelper
from config import Config


class Mapper(object):
    log = None
    model = None

    @classmethod
    async def list_record(cls, **kwargs):
        """
        通过查询条件获取数据，kwargs的key为参数名, value为参数值
        :param kwargs:
        :return:
        """
        try:
            async with async_session() as session:
                sql = cls.query_wrapper(**kwargs)
                result = await session.execute(sql)
                return result.scalars().all()
        except Exception as e:
            # 这边调用cls本身的log参数，写入日志+抛出异常
            cls.log.error(f"获取{cls.model}列表失败, error: {e}")
            raise Exception(f"获取数据失败")

    @classmethod
    async def list_record_with_pagination(cls, page, size, **kwargs):
        """
        通过分页获取数据
        :param page:
        :param size:
        :param kwargs:
        :return:
        """
        try:
            async with async_session() as session:
                sql = cls.query_wrapper(**kwargs)
                return await DatabaseHelper.pagination(page, size, session, sql)
        except Exception as e:
            cls.log.error(f"获取{cls.model}列表失败, error: {e}")
            raise Exception(f"获取数据失败")

    @classmethod
    def query_wrapper(cls, **kwargs):
        condition = [getattr(cls.model, "deleted_at") == 0]
        # 遍历参数，当参数不为None的时候传递
        for k, v in kwargs.items():
            # 判断是否是like的情况 TODO: 这里没支持in查询
            like = isinstance(v, str) and len(v) > 2 and v.startswith("%") and v.endswith("%")
            # 如果是like模式，则使用Model.字段.like 否则用 Model.字段 等于
            DatabaseHelper.where(v, getattr(cls.model, k).like(v) if like else getattr(cls.model, k) == v,
                                 condition)
        return select(cls.model).where(*condition)

    @classmethod
    async def query_record(cls, **kwargs):
        try:
            async with async_session() as session:
                sql = cls.query_wrapper(**kwargs)
                result = await session.execute(sql)
                return result.scalars().first()
        except Exception as e:
            cls.log.error(f"查询{cls.model}失败, error: {e}")
            raise Exception(f"查询记录失败")

    @classmethod
    async def insert_record(cls, model):
        try:
            async with async_session() as session:
                async with session.begin():
                    session.add(model)
                    await session.flush()
                    session.expunge(model)
                    return model
        except Exception as e:
            cls.log.error(f"添加{cls.model}记录失败, error: {e}")
            raise Exception(f"添加记录失败")

    @classmethod
    async def update_record_by_id(cls, user, model, not_null=False):
        try:
            async with async_session() as session:
                async with session.begin():
                    query = cls.query_wrapper(id=model.id)
                    result = await session.execute(query)
                    original = result.scalars().first()
                    if original is None:
                        raise Exception("记录不存在")
                    DatabaseHelper.update_model(original, model, user, not_null)
                    await session.flush()
                    session.expunge(original)
                    return original
        except Exception as e:
            cls.log.error(f"更新{cls.model}记录失败, error: {e}")
            raise Exception(f"更新记录失败")

    @classmethod
    async def delete_record_by_id(cls, user, id):
        """
        逻辑删除
        :param user:
        :param id:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    query = cls.query_wrapper(id=id)
                    result = await session.execute(query)
                    original = result.scalars().first()
                    if original is None:
                        raise Exception("记录不存在")
                    DatabaseHelper.delete_model(original, user)
                    await session.flush()
                    session.expunge(original)
                    return original
        except Exception as e:
            cls.log.error(f"删除{cls.model}记录失败, error: {e}")
            raise Exception(f"删除记录失败")

    @classmethod
    async def delete_by_id(cls, id):
        """
        物理删除
        :param id:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    query = cls.query_wrapper(id=id)
                    result = await session.execute(query)
                    original = result.scalars().first()
                    if original is None:
                        raise Exception("记录不存在")
                    session.delete(original)
        except Exception as e:
            cls.log.error(f"逻辑删除{cls.model}记录失败, error: {e}")
            raise Exception(f"删除记录失败")


def get_dao_path():
    """获取dao目录下所有的xxxDao.py"""
    dao_path_list = []
    for file in os.listdir(Config.DAO_PATH):
        # 拼接目录
        file_path = os.path.join(Config.DAO_PATH, file)
        # 判断过滤, 取有效目录
        if os.path.isdir(file_path) and '__pycache__' not in file:
            from collections import defaultdict
            path_dict = defaultdict(list)
            # 获取目录下所有的xxxDao.py
            for py_file in os.listdir(file_path):
                if py_file.endswith('py') and 'init' not in py_file:
                    path_dict[file].append(py_file.split('.')[0])
            dao_path_list.append(path_dict)
    return dao_path_list


dao_path_list = get_dao_path()
for path in dao_path_list:
    for file_path, pys in path.items():
        # 拼接对应的dao目录
        son_dao_path = os.path.join(Config.DAO_PATH, file_path)
        # 导包时, 默认在这个路径下查找
        sys.path.append(son_dao_path)
        for py in pys:
            # 动态导包进去
            importlib.import_module(py)

Base.metadata.create_all(engine)

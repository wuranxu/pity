from collections import defaultdict
from typing import List

from sqlalchemy import select

from app.models import Session, async_session, DatabaseHelper
from app.models.constructor import Constructor
from app.models.schema.constructor import ConstructorForm, ConstructorIndex
from app.models.test_case import TestCase
from app.utils.logger import Log


class ConstructorDao(object):
    log = Log("ConstructorDao")

    @staticmethod
    async def list_constructor(case_id: int):
        try:
            async with async_session() as session:
                sql = select(Constructor).where(Constructor.case_id == case_id, Constructor.deleted_at == None) \
                    .order_by(Constructor.index, Constructor.updated_at)
                result = await session.execute(sql)
                return result.scalars().all()
        except Exception as e:
            ConstructorDao.log.error(f"获取初始化数据失败, {e}")
            raise Exception(f"获取初始化数据失败, {e}")

    @staticmethod
    async def insert_constructor(data: ConstructorForm, user):
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(Constructor).where(Constructor.case_id == data.case_id, Constructor.name == data.name,
                                                    Constructor.deleted_at == None)
                    result = await session.execute(sql)
                    if result.scalars().first() is not None:
                        raise Exception(f"初始化数据: {data.name}已存在")
                    constructor = Constructor(**data.dict(), user=user)
                    constructor.index = await constructor.get_index(session, data.case_id)
                    session.add(constructor)
        except Exception as e:
            ConstructorDao.log.error(f"新增初始化数据: {data.name}失败, {e}")
            raise Exception(f"新增初始化数据失败, {e}")

    @staticmethod
    async def update_constructor(data: ConstructorForm, user):
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(Constructor).where(Constructor.id == data.id)
                    result = await session.execute(sql)
                    query = result.scalars().first()
                    if query is None:
                        raise Exception(f"数据构造器: {data.name}不存在")
                    DatabaseHelper.update_model(query, data, user)
        except Exception as e:
            ConstructorDao.log.error(f"编辑初始化数据: {data.name}失败, {e}")
            raise Exception(f"编辑初始化数据失败, {e}")

    @staticmethod
    async def delete_constructor(id: int, user):
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(Constructor).where(Constructor.id == id)
                    result = await session.execute(sql)
                    query = result.scalars().first()
                    if query is None:
                        raise Exception(f"数据构造器:{id}不存在")
                    DatabaseHelper.delete_model(query, user)
        except Exception as e:
            ConstructorDao.log.error(f"删除初始化数据: {id}失败, {e}")
            raise Exception(f"删除初始化数据失败, {e}")

    @staticmethod
    def update_constructor_index(data: List[ConstructorIndex]):
        try:
            with Session() as session:
                mappings = [{"id": item.id, "index": item.index} for item in data]
                session.bulk_update_mappings(Constructor, mappings)
                session.commit()
        except Exception as e:
            ConstructorDao.log.error(f"更新数据构造器顺序失败, {e}")
            raise Exception("更新数据构造器顺序失败")

    @staticmethod
    def get_constructor_tree(name: str):
        try:
            with Session() as session:
                # 获取所有构造参数
                if name:
                    constructor = session.query(Constructor).filter(Constructor.public == True,
                                                                    Constructor.name.ilike("%{}%".format(name)),
                                                                    Constructor.deleted_at == None).all()
                else:
                    constructor = session.query(Constructor).filter(Constructor.public == True,
                                                                    Constructor.deleted_at == None).all()
                if not constructor:
                    return []
                temp = defaultdict(list)
                # 建立caseID -> constructor的map
                for c in constructor:
                    temp[c.case_id].append(c)
                testcases = session.query(TestCase).filter(TestCase.id.in_(temp.keys())).all()
                testcase_info = {t.id: t for t in testcases}
                result = []
                for k, v in temp.items():
                    result.append({
                        "key": f"caseId_{k}",
                        "disabled": True,
                        "title": testcase_info[k].name,
                        "children": [
                            {"key": f"constructor_{x.id}", "title": x.name, "value": f"constructor_{x.id}"} for x in v
                        ],
                    })
                return result
        except Exception as e:
            ConstructorDao.log.error(f"获取构造数据树失败, {e}")
            raise Exception("获取构造数据失败")

    @staticmethod
    def get_constructor_data(id_: int):
        with Session() as session:
            data = session.query(Constructor).filter_by(id=id_, deleted_at=None).first()
            if data is None:
                raise Exception("构造数据不存在")
            return data

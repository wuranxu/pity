from collections import defaultdict
from typing import List

from sqlalchemy import select, update

from app.crud import Mapper, ModelWrapper
from app.models import async_session
from app.models.constructor import Constructor
from app.models.test_case import TestCase
from app.schema.constructor import ConstructorForm, ConstructorIndex


@ModelWrapper(Constructor)
class ConstructorDao(Mapper):

    @staticmethod
    async def list_constructor(case_id: int) -> List[Constructor]:
        """
        根据用例id获取数据构造器列表（包括前后置条件）
        :param case_id:
        :return:
        """
        try:
            async with async_session() as session:
                sql = select(Constructor).where(Constructor.case_id == case_id, Constructor.deleted_at == 0) \
                    .order_by(Constructor.index, Constructor.updated_at)
                result = await session.execute(sql)
                return result.scalars().all()
        except Exception as e:
            ConstructorDao.__log__.error(f"获取初始化数据失败, {e}")
            raise Exception(f"获取初始化数据失败, {e}")

    @staticmethod
    async def insert_constructor(data: ConstructorForm, user_id: int) -> None:
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(Constructor).where(Constructor.case_id == data.case_id, Constructor.name == data.name,
                                                    Constructor.deleted_at == 0)
                    result = await session.execute(sql)
                    if result.scalars().first() is not None:
                        raise Exception(f"{data.name}已存在")
                    constructor = Constructor(**data.dict(), user_id=user_id)
                    constructor.index = await constructor.get_index(session, data.case_id)
                    session.add(constructor)
        except Exception as e:
            ConstructorDao.__log__.error(f"新增前/后置条件: {data.name}失败, {e}")
            raise Exception(f"新增前/后置条件失败, {e}")

    @staticmethod
    async def update_constructor(data: ConstructorForm, user_id: int) -> None:
        """
        更新前后置条件
        :param data:
        :param user_id:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(Constructor).where(Constructor.id == data.id)
                    result = await session.execute(sql)
                    query = result.scalars().first()
                    if query is None:
                        raise Exception(f"{data.name}不存在")
                    ConstructorDao.update_model(query, data, user_id)
        except Exception as e:
            ConstructorDao.__log__.error(f"编辑前后置条件: {data.name}失败, {e}")
            raise Exception(f"编辑前后置条件失败, {e}")

    @classmethod
    async def delete_constructor(cls, id: int, user_id: int) -> None:
        """
        删除前后置条件
        :param id:
        :param user_id:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(Constructor).where(Constructor.id == id)
                    result = await session.execute(sql)
                    query = result.scalars().first()
                    if query is None:
                        raise Exception(f"前后置条件{id}不存在")
                    ConstructorDao.delete_model(query, user_id)
        except Exception as e:
            cls.__log__.error(f"删除前后置条件: {id}失败, {e}")
            raise Exception(f"删除前后置条件失败, {e}")

    @classmethod
    async def update_constructor_index(cls, data: List[ConstructorIndex]) -> None:
        """
        更改前后置条件顺序
        :param data:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    for item in data:
                        await session.execute(
                            update(Constructor).where(Constructor.id == item.id).values(index=item.index))
        except Exception as e:
            cls.__log__.error(f"更新前后置条件顺序失败, {e}")
            raise Exception("更新前后置条件顺序失败")

    @classmethod
    async def get_constructor_tree(cls, name: str, suffix: bool) -> List[dict]:
        try:
            async with async_session() as session:
                # 获取所有构造参数
                search = [Constructor.public == True, Constructor.suffix == suffix, Constructor.deleted_at == 0]
                if name:
                    search.append(Constructor.name.like("%{}%".format(name)))
                query = await session.execute(select(Constructor).where(*search))
                constructor = query.scalars().all()
                if not constructor:
                    return []
                temp = defaultdict(list)
                # 建立caseID -> constructor的map
                for c in constructor:
                    temp[c.case_id].append(c)
                query = await session.execute(select(TestCase).where(TestCase.id.in_(temp.keys())))
                testcases = query.scalars().all()
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
            cls.__log__.error(f"获取前后置条件树失败, {e}")
            raise Exception("获取前后置条件失败")

    @staticmethod
    async def get_constructor_data(id_: int) -> Constructor:
        """
        根据构造方法id获取构造方法数据
        :param id_:
        :return:
        """
        async with async_session() as session:
            query = await session.execute(select(Constructor).where(Constructor.id == id_, Constructor.deleted_at == 0))
            data = query.scalars().first()
            if data is None:
                raise Exception("前后置条件不存在")
            return data

    @staticmethod
    async def get_case_and_constructor(constructor_type: int, suffix: bool) -> List[dict]:
        """
        根据构造类型返回构造方法树
        :param constructor_type:
        :param suffix:
        :return:
        """
        ans = list()
        async with async_session() as session:
            # 此处存放case_id => 前置条件的映射
            constructors = defaultdict(list)
            # 根据传入的前后置条件类型，找出所有前置条件, 类型一致，共享开关打开，并未被删除
            query = await session.execute(
                select(Constructor).where(
                    Constructor.suffix == suffix,
                    Constructor.type == constructor_type,
                    Constructor.public == True,
                    Constructor.deleted_at == 0))
            # 并把这些前置条件放到constructors里面
            for q in query.scalars().all():
                constructors[q.case_id].append({
                    "title": q.name,
                    "key": f"constructor_{q.id}",
                    "value": f"constructor_{q.id}",
                    "isLeaf": True,
                    # 这里是为了拿到具体的代码，因为树一般只有name和id，我们这还需要其他数据
                    "constructor_json": q.constructor_json,
                })
            if len(constructors.keys()) == 0:
                return []
            # 二次查询，查出有前置条件的case
            query = await session.execute(
                select(TestCase).where(TestCase.id.in_(constructors.keys()), TestCase.deleted_at == 0))
            # 构造树，要知道children已经构建好了，就在constructors里面
            for q in query.scalars().all():
                # 把用例id放入cs_list，这里就不用原生join了
                ans.append({
                    "title": q.name,
                    "key": f"caseId_{q.id}",
                    "disabled": True,
                    "children": constructors[q.id]
                })
        return ans

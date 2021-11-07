import json
from collections import defaultdict
from typing import List

from sqlalchemy import desc
from sqlalchemy.future import select

from app.dao.test_case.ConstructorDao import ConstructorDao
from app.dao.test_case.TestCaseAssertsDao import TestCaseAssertsDao
from app.dao.test_case.TestCaseDirectory import PityTestcaseDirectoryDao
from app.dao.test_case.TestcaseDataDao import PityTestcaseDataDao
from app.models import Session, DatabaseHelper, async_session
from app.models.constructor import Constructor
from app.models.schema.testcase_schema import TestCaseForm
from app.models.test_case import TestCase
from app.utils.logger import Log


class TestCaseDao(object):
    log = Log("TestCaseDao")

    @staticmethod
    async def list_test_case(directory_id: int = None, name: str = "", create_user: str = None):
        try:
            filters = [TestCase.deleted_at == None]
            if directory_id:
                parents = await PityTestcaseDirectoryDao.get_directory_son(directory_id)
                filters = [TestCase.deleted_at == None, TestCase.directory_id.in_(parents)]
                if name:
                    filters.append(TestCase.name.like(f"%{name}%"))
                if create_user:
                    filters.append(TestCase.create_user == create_user)
            async with async_session() as session:
                sql = select(TestCase).where(*filters).order_by(TestCase.name.asc())
                result = await session.execute(sql)
                return result.scalars().all()
        except Exception as e:
            TestCaseDao.log.error(f"获取测试用例失败: {str(e)}")
            raise Exception(f"获取测试用例失败: {str(e)}")

    @staticmethod
    async def get_test_case_by_directory_id(directory_id: int):
        try:
            async with async_session() as session:
                sql = select(TestCase).where(TestCase.deleted_at == None,
                                             TestCase.directory_id == directory_id).order_by(TestCase.name.asc())
                result = await session.execute(sql)
                ans = []
                case_map = dict()
                for item in result.scalars():
                    ans.append({"title": item.name, "key": "testcase_{}".format(item.id), "children": []})
                    case_map[item.id]=item.name
                return ans, case_map
        except Exception as e:
            TestCaseDao.log.error(f"获取测试用例失败: {str(e)}")
            raise Exception(f"获取测试用例失败: {str(e)}")

    @staticmethod
    def get_tree(case_list):
        result = defaultdict(list)
        # 获取目录->用例的映射关系
        for cs in case_list:
            result[cs.catalogue].append(cs)

        keys = sorted(result.keys())
        tree = [dict(key=f"cat_{key}",
                     children=[{"key": f"case_{child.id}", "title": child.name,
                                "total": TestCaseDao.get_case_children_length(child.id),
                                "children": TestCaseDao.get_case_children(child.id)} for child in result[key]],
                     title=key, total=len(result[key])) for key in keys]
        return tree

    @staticmethod
    def get_case_children(case_id: int):
        data, err = TestCaseAssertsDao.list_test_case_asserts(case_id)
        if err:
            raise err
        return [dict(key=f"asserts_{d.id}", title=d.name, case_id=case_id) for d in data]

    @staticmethod
    def get_case_children_length(case_id: int):
        data, err = TestCaseAssertsDao.list_test_case_asserts(case_id)
        if err:
            raise err
        return len(data)

    @staticmethod
    def insert_test_case(test_case, user):
        """

        :param user: 创建人
        :param test_case: 测试用例
        :return:
        """
        try:
            with Session() as session:
                data = session.query(TestCase).filter_by(name=test_case.get("name"),
                                                         directory_id=test_case.get("directory_id"),
                                                         deleted_at=None).first()
                if data is not None:
                    raise Exception("用例已存在")
                cs = TestCase(**test_case, create_user=user)
                session.add(cs)
                session.commit()
                session.refresh(cs)
                return cs.id
        except Exception as e:
            TestCaseDao.log.error(f"添加用例失败: {str(e)}")
            raise Exception(f"添加用例失败: {str(e)}")

    @staticmethod
    def update_test_case(test_case: TestCaseForm, user):
        """

        :param user: 修改人
        :param test_case: 测试用例
        :return:
        """
        try:
            with Session() as session:
                data = session.query(TestCase).filter_by(id=test_case.id, deleted_at=None).first()
                if data is None:
                    raise Exception("用例不存在")
                DatabaseHelper.update_model(data, test_case, user)
                session.commit()
                session.refresh(data)
                return data
        except Exception as e:
            TestCaseDao.log.error(f"编辑用例失败: {str(e)}")
            raise Exception(f"编辑用例失败: {str(e)}")

    @staticmethod
    async def query_test_case(case_id: int) -> dict:
        try:
            async with async_session() as session:
                sql = select(TestCase).where(TestCase.id == case_id, TestCase.deleted_at == None)
                result = await session.execute(sql)
                data = result.scalars().first()
                if data is None:
                    raise Exception("用例不存在")
                # 获取断言部分
                asserts, _ = await TestCaseAssertsDao.async_list_test_case_asserts(data.id)
                # 获取数据构造器
                constructors = await ConstructorDao.list_constructor(case_id)
                constructors_case = await TestCaseDao.query_test_case_by_constructors(constructors)
                test_data = await PityTestcaseDataDao.list_testcase_data(case_id)
                return dict(asserts=asserts, constructors=constructors, case=data, constructors_case=constructors_case,
                            test_data=test_data)
        except Exception as e:
            TestCaseDao.log.error(f"查询用例失败: {str(e)}")
            raise Exception(f"查询用例失败: {str(e)}")

    @staticmethod
    async def query_test_case_by_constructors(constructors: List[Constructor]):
        try:
            # 找到所有用例名称为
            constructors = [json.loads(x.constructor_json).get("case_id") for x in constructors if x.type == 0]
            async with async_session() as session:
                sql = select(TestCase).where(TestCase.id.in_(constructors), TestCase.deleted_at == None)
                result = await session.execute(sql)
                data = result.scalars().all()
                return {x.id: x for x in data}
        except Exception as e:
            TestCaseDao.log.error(f"查询用例失败: {str(e)}")
            raise Exception(f"查询用例失败: {str(e)}")

    @staticmethod
    async def async_query_test_case(case_id) -> [TestCase, str]:
        try:
            async with async_session() as session:
                result = await session.execute(
                    select(TestCase).where(TestCase.id == case_id, TestCase.deleted_at == None))
                data = result.scalars().first()
                if data is None:
                    return None, "用例不存在"
                return data, None
        except Exception as e:
            TestCaseDao.log.error(f"查询用例失败: {str(e)}")
            return None, f"查询用例失败: {str(e)}"

    @staticmethod
    def list_testcase_tree(projects) -> [List, dict]:
        try:
            result = []
            project_map = {}
            project_index = {}
            for p in projects:
                project_map[p.id] = p.name
                result.append({
                    "label": p.name,
                    "value": p.id,
                    "key": p.id,
                    "children": [],
                })
                project_index[p.id] = len(result) - 1
            with Session() as session:
                data = session.query(TestCase).filter(TestCase.project_id.in_(project_map.keys()),
                                                      TestCase.deleted_at == None).all()

                for d in data:
                    result[project_index[d.project_id]]["children"].append({
                        "label": d.name,
                        "value": d.id,
                        "key": d.id,
                    })
                return result
        except Exception as e:
            TestCaseDao.log.error(f"获取用例列表失败: {str(e)}")
            raise Exception("获取用例列表失败")

    @staticmethod
    def select_constructor(case_id: int):
        """
        通过case_id获取用例构造数据
        :param case_id:
        :return:
        """
        try:
            with Session() as session:
                data = session.query(Constructor).filter_by(case_id=case_id, deleted_at=None).order_by(
                    desc(Constructor.created_at)).all()
                return data
        except Exception as e:
            TestCaseDao.log.error(f"查询构造数据失败: {str(e)}")

    @staticmethod
    async def async_select_constructor(case_id: int) -> List[Constructor]:
        """
        异步获取用例构造数据
        :param case_id:
        :return:
        """
        try:
            async with async_session() as session:
                sql = select(Constructor).where(Constructor.case_id == case_id,
                                                Constructor.deleted_at == None).order_by(Constructor.created_at)
                data = await session.execute(sql)
                return data.scalars().all()
        except Exception as e:
            TestCaseDao.log.error(f"查询构造数据失败: {str(e)}")

    @staticmethod
    async def collect_data(case_id: int, data: List):
        """
        收集以case_id为前置条件的数据(后置暂时不支持)
        :param data:
        :param case_id:
        :return:
        """
        # 先获取数据构造器（前置条件）
        pre = dict(id=f"pre_{case_id}", label="前置条件", children=list())
        await TestCaseDao.collect_constructor(case_id, pre)
        data.append(pre)

        # 获取断言
        asserts = dict(id=f"asserts_{case_id}", label="断言", children=list())
        await TestCaseDao.collect_asserts(case_id, asserts)
        data.append(asserts)

    @staticmethod
    async def collect_constructor(case_id, parent):
        constructors = await TestCaseDao.async_select_constructor(case_id)
        for c in constructors:
            temp = dict(id=f"constructor_{c.id}", label=f"{c.name}", children=list())
            if c.type == 0:
                # 说明是用例，继续递归
                temp["label"] = "[CASE]: " + temp["label"]
                json_data = json.loads(c.constructor_json)
                await TestCaseDao.collect_data(json_data.get("case_id"), temp.get("children"))
            elif c.type == 1:
                temp["label"] = "[SQL]: " + temp["label"]
            elif c.type == 2:
                temp["label"] = "[REDIS]: " + temp["label"]
            # 否则正常添加数据
            parent.get("children").append(temp)

    @staticmethod
    async def collect_asserts(case_id, parent):
        asserts, err = await TestCaseAssertsDao.async_list_test_case_asserts(case_id)
        if err:
            raise Exception("获取断言数据失败")
        for a in asserts:
            temp = dict(id=f"assert_{a.id}", label=f"{a.name}", children=list())
            parent.get("children").append(temp)

    @staticmethod
    async def get_xmind_data(case_id: int):
        result = dict()
        data = await TestCaseDao.query_test_case(case_id)
        cs = data.get("case")
        # 开始解析测试数据
        result.update(dict(id=f"case_{case_id}", label=f"{cs.name}({cs.id})"))
        children = list()
        await TestCaseDao.collect_data(case_id, children)
        result["children"] = children
        return result

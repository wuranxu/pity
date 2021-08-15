import json
from collections import defaultdict
from typing import List

from sqlalchemy import desc
from sqlalchemy.future import select

from app.dao.test_case.TestCaseAssertsDao import TestCaseAssertsDao
from app.models import Session, update_model, async_session
from app.models.constructor import Constructor
from app.models.test_case import TestCase
from app.routers.testcase.testcase_schema import TestCaseForm
from app.utils.logger import Log


class TestCaseDao(object):
    log = Log("TestCaseDao")

    @staticmethod
    def list_test_case(project_id):
        try:
            with Session() as session:
                case_list = session.query(TestCase).filter_by(project_id=project_id, deleted_at=None).order_by(
                    TestCase.name.asc()).all()
                return TestCaseDao.get_tree(case_list), None
        except Exception as e:
            TestCaseDao.log.error(f"获取测试用例失败: {str(e)}")
            return [], f"获取测试用例失败: {str(e)}"

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
                                                         project_id=test_case.get("project_id"),
                                                         deleted_at=None).first()
                if data is not None:
                    return "用例已存在"
                cs = TestCase(**test_case, create_user=user)
                session.add(cs)
                session.commit()
        except Exception as e:
            TestCaseDao.log.error(f"添加用例失败: {str(e)}")
            return f"添加用例失败: {str(e)}"
        return None

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
                    return "用例不存在"
                update_model(data, test_case, user)
                session.commit()
        except Exception as e:
            TestCaseDao.log.error(f"编辑用例失败: {str(e)}")
            return f"编辑用例失败: {str(e)}"
        return None

    @staticmethod
    def query_test_case(case_id) -> [TestCase, str]:
        try:
            with Session() as session:
                data = session.query(TestCase).filter_by(id=case_id, deleted_at=None).first()
                if data is None:
                    return None, "用例不存在"
                return data, None
        except Exception as e:
            TestCaseDao.log.error(f"查询用例失败: {str(e)}")
            return None, f"查询用例失败: {str(e)}"

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
        data, err = TestCaseDao.query_test_case(case_id)
        if err:
            raise Exception(err)
        # 开始解析测试数据
        result.update(dict(id=f"case_{case_id}", label=f"{data.name}({data.id})"))
        children = list()
        await TestCaseDao.collect_data(case_id, children)
        result["children"] = children
        return result

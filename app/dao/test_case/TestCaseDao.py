from collections import defaultdict
from typing import List

from sqlalchemy import desc

from app.dao.test_case.TestCaseAssertsDao import TestCaseAssertsDao
from app.models import Session, update_model
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

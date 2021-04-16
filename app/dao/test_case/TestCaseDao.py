from collections import defaultdict

from app.models import db
from app.models.test_case import TestCase
from app.utils.logger import Log


class TestCaseDao(object):
    log = Log("TestCaseDao")

    @staticmethod
    def list_test_case(project_id):
        try:
            case_list = TestCase.query.filter_by(project_id=project_id, deleted_at=None).order_by(
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
                     children=[{"key": f"case_{child.id}", "title": child.name} for child in result[key]],
                     title=key, total=len(result[key])) for key in keys]
        return tree

    @staticmethod
    def insert_test_case(test_case, user):
        """

        :param user: 创建人
        :param test_case: 测试用例
        :return:
        """
        try:
            data = TestCase.query.filter_by(name=test_case.get("name"), project_id=test_case.get("project_id"),
                                            deleted_at=None).first()
            if data is not None:
                return "用例已存在"
            cs = TestCase(**test_case, create_user=user)
            db.session.add(cs)
            db.session.commit()
        except Exception as e:
            TestCaseDao.log.error(f"添加用例失败: {str(e)}")
            return f"添加用例失败: {str(e)}"
        return None

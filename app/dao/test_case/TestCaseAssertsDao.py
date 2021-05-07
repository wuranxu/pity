from sqlalchemy import asc

from app.models import Session
from app.models.testcase_asserts import TestCaseAsserts
from app.utils.logger import Log


class TestCaseAssertsDao(object):
    log = Log("TestCaseAssertsDao")

    @staticmethod
    def list_test_case_asserts(case_id: int):
        try:
            with Session() as session:
                case_list = session.query(TestCaseAsserts).filter_by(case_id=case_id, deleted_at=None).order_by(
                    asc(TestCaseAsserts.name)).all()
                return case_list, None
        except Exception as e:
            TestCaseAssertsDao.log.error(f"获取用例断言失败: {str(e)}")
            return [], f"获取用例断言失败: {str(e)}"

    @staticmethod
    def insert_test_case_asserts(id, name, case_id, assert_type, expected, actually, user):
        try:
            with Session() as session:
                exists = session.query(TestCaseAsserts).filter_by(case_id=case_id, name=name, deleted_at=None).first()
                if exists is not None:
                    # 说明断言存在
                    raise Exception("断言信息已存在, 请检查")
                new_assert = TestCaseAsserts(id, name, case_id, assert_type, expected, actually, user)
                session.add(new_assert)
                session.commit()
        except Exception as e:
            TestCaseAssertsDao.log.error(f"新增用例断言失败: {str(e)}")
            return f"新增用例断言失败: {str(e)}"
        return None

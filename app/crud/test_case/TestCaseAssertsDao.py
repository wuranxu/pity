from sqlalchemy import asc, select

from app.crud import Mapper
from app.models import Session, async_session, DatabaseHelper
from app.schema.testcase_schema import TestCaseAssertsForm
from app.models.testcase_asserts import TestCaseAsserts
from app.utils.decorator import dao
from app.utils.logger import Log


@dao(TestCaseAsserts, Log("TestCaseAssertsDao"))
class TestCaseAssertsDao(Mapper):
    # log = Log("TestCaseAssertsDao")

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

    @classmethod
    async def async_list_test_case_asserts(cls, case_id: int):
        try:
            async with async_session() as session:
                sql = select(TestCaseAsserts).where(TestCaseAsserts.case_id == case_id,
                                                    TestCaseAsserts.deleted_at == 0).order_by(TestCaseAsserts.name)
                case_list = await session.execute(sql)
                return case_list.scalars().all(), None
        except Exception as e:
            cls.log.error(f"获取用例断言失败: {str(e)}")
            return [], f"获取用例断言失败: {str(e)}"

    @staticmethod
    async def insert_test_case_asserts(form: TestCaseAssertsForm, user: int):
        try:
            ans = None
            async with async_session() as session:
                async with session.begin():
                    sql = select(TestCaseAsserts).where(TestCaseAsserts.case_id == form.case_id,
                                                        TestCaseAsserts.name == form.name,
                                                        TestCaseAsserts.deleted_at == 0)
                    result = await session.execute(sql)
                    data = result.scalars().first()
                    if data is not None:
                        raise Exception("断言信息已存在, 请检查")
                    new_assert = TestCaseAsserts(**form.dict(), user=user)
                    session.add(new_assert)
                    await session.flush()
                    await session.refresh(new_assert)
                    session.expunge(new_assert)
                    return new_assert
            return ans
        except Exception as e:
            TestCaseAssertsDao.log.error(f"新增用例断言失败, error: {e}")
            raise Exception(f"新增用例断言失败, {e}")

    @staticmethod
    async def update_test_case_asserts(form: TestCaseAssertsForm, user: int):
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(TestCaseAsserts).where(TestCaseAsserts.id == form.id,
                                                        TestCaseAsserts.deleted_at == 0)
                    result = await session.execute(sql)
                    data = result.scalars().first()
                    if data is None:
                        raise Exception("断言信息不存在, 请检查")
                    DatabaseHelper.update_model(data, form, user)
                    await session.flush()
                    session.expunge(data)
                    return data
        except Exception as e:
            TestCaseAssertsDao.log.error(f"编辑用例断言失败, error: {e}")
            raise Exception(f"编辑用例断言失败, {e}")

    @staticmethod
    async def delete_test_case_asserts(id: int, user: int):
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(TestCaseAsserts).where(TestCaseAsserts.id == id,
                                                        TestCaseAsserts.deleted_at == 0)
                    result = await session.execute(sql)
                    data = result.scalars().first()
                    if data is None:
                        raise Exception("断言信息不存在, 请检查")
                    DatabaseHelper.delete_model(data, user)
                    await session.flush()
        except Exception as e:
            TestCaseAssertsDao.log.error(f"编辑用例断言失败, error: {e}")
            raise Exception(f"编辑用例断言失败, {e}")

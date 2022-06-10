from sqlalchemy import Column, INT, String, TEXT

from app.models.basic import PityBase


class TestCaseAsserts(PityBase):
    __tablename__ = "pity_testcase_asserts"
    name = Column(String(32), nullable=False)
    case_id = Column(INT, index=True)
    assert_type = Column(String(16), comment="equal: 等于 not_equal: 不等于 in: 属于")
    expected = Column(TEXT, nullable=False)
    actually = Column(TEXT, nullable=False)
    __fields__ = (name, case_id, assert_type, expected, actually)
    __tag__ = "断言"
    __alias__ = dict(name="名称", case_id="测试用例", assert_type="断言类型", expected="预期结果", actually="实际结果")

    def __init__(self, name, case_id, assert_type, expected, actually, user_id, id=None):
        super().__init__(user_id, id)
        self.name = name
        self.case_id = case_id
        self.assert_type = assert_type
        self.expected = expected
        self.actually = actually

from datetime import datetime

from sqlalchemy import Column, INT, String, DATETIME, TEXT

from app.models import Base


class TestCaseAsserts(Base):
    __tablename__ = "pity_testcase_asserts"
    id = Column(INT, primary_key=True)
    name = Column(String(32), nullable=False)
    case_id = Column(INT, index=True)
    assert_type = Column(String(16), comment="equal: 等于 not_equal: 不等于 in: 属于")
    expected = Column(TEXT, nullable=False)
    actually = Column(TEXT, nullable=False)
    created_at = Column(DATETIME, nullable=False)
    updated_at = Column(DATETIME, nullable=False)
    deleted_at = Column(DATETIME)
    create_user = Column(INT, nullable=False)
    update_user = Column(INT, nullable=False)

    def __init__(self, name, case_id, assert_type, expected, actually, user, id=0):
        self.id = id
        self.name = name
        self.case_id = case_id
        self.assert_type = assert_type
        self.expected = expected
        self.actually = actually
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.create_user = user
        self.update_user = user

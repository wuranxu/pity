from datetime import datetime

from sqlalchemy import Column, INT, String, UniqueConstraint

from app.models.basic import PityBase
from app.schema.testcase_directory import PityTestcaseDirectoryForm


class PityTestcaseDirectory(PityBase):
    """
    用例目录表
    """
    __tablename__ = 'pity_testcase_directory'
    # 联合索引，防止同一层次出现同名目录
    __table_args__ = (
        UniqueConstraint('project_id', 'name', 'parent', 'deleted_at'),
    )
    id = Column(INT, primary_key=True)
    project_id = Column(INT, index=True)

    # 目录名称
    name = Column(String(18), nullable=False)

    # 目录上级目录，如果没有则为None
    parent = Column(INT)

    def __init__(self, form: PityTestcaseDirectoryForm, user):
        super().__init__(user)
        self.project_id = form.project_id
        self.name = form.name
        self.parent = form.parent
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.create_user = user
        self.update_user = user

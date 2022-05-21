"""
数据构造器表, 包含前置条件和后置条件
"""

from sqlalchemy import Column, INT, String, BOOLEAN, UniqueConstraint, TEXT, select, desc

from app.models.basic import PityBase


class Constructor(PityBase):
    __tablename__ = 'pity_constructor'
    __table_args__ = (
        UniqueConstraint('case_id', 'suffix', 'name', 'deleted_at'),
    )

    type = Column(INT, default=0, comment="0: testcase 1: sql 2: redis 3: py脚本 4: 其它")
    name = Column(String(64), comment="数据初始化描述")
    enable = Column(BOOLEAN, default=True, nullable=False)
    constructor_json = Column(TEXT, nullable=False)
    value = Column(String(16), comment="返回值")
    case_id = Column(INT, nullable=False, comment="所属用例id")
    public = Column(BOOLEAN, default=False, comment="是否共享")
    index = Column(INT, comment="前置条件顺序")
    # 2021-12-18 是否是后置条件
    suffix = Column(BOOLEAN, default=False, comment="是否是后置条件，默认为否")

    def __init__(self, type, name, enable, constructor_json, case_id, public, user_id, value="", suffix=False, id=None,
                 index=0):
        super().__init__(user_id, id)
        self.type = type
        self.name = name
        self.enable = enable
        self.constructor_json = constructor_json
        self.case_id = case_id
        self.public = public
        self.value = value
        self.suffix = suffix
        self.index = index

    @staticmethod
    async def get_index(session, case_id, suffix=False):
        sql = select(Constructor).where(
            Constructor.deleted_at == 0, Constructor.case_id == case_id,
            Constructor.suffix == suffix,
        ).order_by(desc(Constructor.index))
        data = await session.execute(sql)
        query = data.scalars().first()
        # 如果没有查出来前/后置条件，那么给他0
        if query is None:
            return 0
        return query.index + 1

    def __str__(self):
        return f"[{'后置条件' if self.suffix else '前置条件'}: {self.name}]({self.id}))"

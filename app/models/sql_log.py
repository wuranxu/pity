from sqlalchemy import Column, String, INT

from app.models.basic import PityBase
from app.models.database import PityDatabase


class PitySQLHistory(PityBase):
    __tablename__ = "pity_sql_history"
    sql = Column(String(1024), comment="sql语句")
    elapsed = Column(INT, comment="请求耗时")
    database_id = Column(INT, comment="操作数据库id")
    database: PityDatabase

    def __init__(self, sql, elapsed, database_id, user):
        super().__init__(user)
        self.sql = sql
        self.elapsed = elapsed
        self.database_id = database_id

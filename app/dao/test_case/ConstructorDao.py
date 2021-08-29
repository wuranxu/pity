from sqlalchemy import select

from app.models import Session, async_session
from app.models.constructor import Constructor
from app.models.schema.constructor import ConstructorForm
from app.models.test_case import TestCase
from app.utils.logger import Log
from collections import defaultdict


class ConstructorDao(object):
    log = Log("ConstructorDao")

    @staticmethod
    async def list_constructor(case_id: int):
        try:
            async with async_session() as session:
                sql = select(Constructor).where(Constructor.case_id == case_id, Constructor.deleted_at == None) \
                    .order_by(Constructor.created_at)
                result = await session.execute(sql)
                return result.scalars().all()
        except Exception as e:
            ConstructorDao.log.error(f"获取初始化数据失败, {e}")
            raise Exception(f"获取初始化数据失败, {e}")

    @staticmethod
    def insert_constructor(data: ConstructorForm, user):
        try:
            with Session() as session:
                query = session.query(Constructor).filter_by(
                    case_id=data.case_id, name=data.name, deleted_at=None).first()
                if query is not None:
                    return f"初始化数据: {data.name}已存在"
                config = Constructor(**data.dict(), user=user)
                session.add(config)
                session.commit()
        except Exception as e:
            ConstructorDao.log.error(f"新增初始化数据: {data.name}失败, {e}")
            raise Exception("新增初始化数据失败")

    @staticmethod
    def get_constructor_tree(name: str):
        try:
            with Session() as session:
                # 获取所有构造参数
                if name:
                    constructor = session.query(Constructor).filter(Constructor.public == True,
                                                                    Constructor.name.ilike("%{}%".format(name)),
                                                                    Constructor.deleted_at == None).all()
                else:
                    constructor = session.query(Constructor).filter(Constructor.public == True,
                                                                    Constructor.deleted_at == None).all()
                if not constructor:
                    return []
                temp = defaultdict(list)
                # 建立caseID -> constructor的map
                for c in constructor:
                    temp[c.case_id].append(c)
                testcases = session.query(TestCase).filter(TestCase.id.in_(temp.keys())).all()
                testcase_info = {t.id: t for t in testcases}
                result = []
                for k, v in temp.items():
                    result.append({
                        "key": f"caseId_{k}",
                        "disabled": True,
                        "title": testcase_info[k].name,
                        "children": [
                            {"key": f"constructor_{x.id}", "title": x.name, "value": f"constructor_{x.id}"} for x in v
                        ],
                    })
                return result
        except Exception as e:
            ConstructorDao.log.error(f"获取构造数据树失败, {e}")
            raise Exception("获取构造数据失败")

    @staticmethod
    def get_constructor_data(id_: int):
        with Session() as session:
            data = session.query(Constructor).filter_by(id=id_, deleted_at=None).first()
            if data is None:
                raise Exception("构造数据不存在")
            return data

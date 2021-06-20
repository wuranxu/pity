from datetime import datetime

from sqlalchemy import desc

from app.models import Session, update_model
from app.models.environment import Environment
from app.models.schema.environment import EnvironmentForm
from app.utils.logger import Log


class EnvironmentDao(object):
    log = Log("EnvironmentDao")

    @staticmethod
    def insert_env(data: EnvironmentForm, user):
        try:
            with Session() as session:
                query = session.query(Environment).filter_by(name=data.name, deleted_at=None).first()
                if query is not None:
                    return f"环境{data.name}已存在"
                env = Environment(**data.dict(), user=user)
                session.add(env)
                session.commit()
        except Exception as e:
            EnvironmentDao.log.error(f"新增环境: {data.name}失败, {e}")
            return f"新增环境: {data.name}失败, {str(e)}"
        return None

    @staticmethod
    def update_env(data: EnvironmentForm, user):
        try:
            with Session() as session:
                query = session.query(Environment).filter_by(id=data.id, deleted_at=None).first()
                if query is None:
                    return f"环境{data.name}不存在"
                update_model(query, data, user)
                session.commit()
        except Exception as e:
            EnvironmentDao.log.error(f"编辑环境失败: {str(e)}")
            return f"编辑环境失败: {str(e)}"
        return None

    @staticmethod
    def list_env(page, size, name=None):
        try:
            search = [Environment.deleted_at == None]
            with Session() as session:
                if name:
                    search.append(Environment.name.ilike("%{}%".format(name)))
                data = session.query(Environment).filter(*search)
                total = data.count()
                return data.order_by(desc(Environment.created_at)).offset((page - 1) * size).limit(
                    size).all(), total, None
        except Exception as e:
            EnvironmentDao.log.error(f"获取环境列表失败, {str(e)}")
            return [], 0, f"获取环境列表失败, {str(e)}"

    @staticmethod
    def delete_env(id, user):
        try:
            with Session() as session:
                query = session.query(Environment).filter_by(id=id).first()
                if query is None:
                    return f"环境{id}不存在"
                query.deleted_at = datetime.now()
                query.update_user = user
                session.commit()
        except Exception as e:
            EnvironmentDao.log.error(f"删除环境失败: {str(e)}")
            return f"删除环境失败: {str(e)}"
        return None

from datetime import datetime

from sqlalchemy import desc

from app.models import Session, update_model
from app.models.gconfig import GConfig
from app.models.schema.gconfig import GConfigForm
from app.utils.logger import Log


class GConfigDao(object):
    log = Log("GConfigDao")

    @staticmethod
    def insert_gconfig(data: GConfigForm, user):
        try:
            with Session() as session:
                query = session.query(GConfig).filter_by(env=data.env, key=data.key, deleted_at=None).first()
                if query is not None:
                    return f"变量: {data.key}已存在"
                config = GConfig(**data.dict(), user=user)
                session.add(config)
                session.commit()
        except Exception as e:
            GConfigDao.log.error(f"新增变量: {data.key}失败, {e}")
            return f"新增变量: {data.key}失败, {str(e)}"
        return None

    @staticmethod
    def update_gconfig(data: GConfigForm, user):
        try:
            with Session() as session:
                query = session.query(GConfig).filter_by(id=data.id, deleted_at=None).first()
                if query is None:
                    return f"变量{data.key}不存在"
                update_model(query, data, user)
                session.commit()
        except Exception as e:
            GConfigDao.log.error(f"编辑变量失败: {str(e)}")
            return f"编辑变量失败: {str(e)}"
        return None

    @staticmethod
    def list_gconfig(page, size, env=None, key=None):
        try:
            search = [GConfig.deleted_at == None]
            with Session() as session:
                if env:
                    search.append(GConfig.env == env)
                if key:
                    search.append(GConfig.key.ilike("%{}%".format(key)))
                data = session.query(GConfig).filter(*search)
                total = data.count()
                return data.order_by(desc(GConfig.created_at)).offset((page - 1) * size).limit(
                    size).all(), total, None
        except Exception as e:
            GConfigDao.log.error(f"获取变量列表失败, {str(e)}")
            return [], 0, f"获取变量列表失败, {str(e)}"

    @staticmethod
    def delete_gconfig(id, user):
        try:
            with Session() as session:
                query = session.query(GConfig).filter_by(id=id).first()
                if query is None:
                    return f"变量{id}不存在"
                query.deleted_at = datetime.now()
                query.update_user = user
                session.commit()
        except Exception as e:
            GConfigDao.log.error(f"删除变量失败: {str(e)}")
            return f"删除变量失败: {str(e)}"
        return None

    @staticmethod
    def get_gconfig_by_key(key: str, env: int = None) -> GConfig:
        try:
            filters = [GConfig.key == key, GConfig.deleted_at == None, GConfig.enable == True]
            if env:
                filters.append(GConfig.env == env)
            with Session() as session:
                return session.query(GConfig).filter(*filters).first()
        except Exception as e:
            raise Exception(f"查询全局变量失败: {str(e)}")

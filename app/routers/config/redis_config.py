from fastapi import Depends

from app.dao.config.RedisConfigDao import PityRedisConfigDao
from app.handler.fatcory import PityResponse
from app.models import DatabaseHelper
from app.models.redis_config import PityRedis
from app.models.schema.redis_config import RedisConfigForm
from app.routers import Permission
from app.routers.config.environment import router
from config import Config


@router.get("/redis/list")
async def list_redis_config(name: str = '', addr: str = '', env: int = None,
                            cluster: bool = None,
                            user_info=Depends(Permission(Config.GUEST))):
    try:
        data = await PityRedisConfigDao.list_record(
            name=DatabaseHelper.like(name), addr=DatabaseHelper.like(addr),
            env=env, cluster=cluster
        )
        return PityResponse.success(data=PityResponse.model_to_list(data))
    except Exception as err:
        return PityResponse.failed(err)


@router.post("/redis/insert")
async def insert_redis_config(form: RedisConfigForm,
                              user_info=Depends(Permission(Config.ADMIN))):
    try:
        query = await PityRedisConfigDao.query_record(name=form.name, env=form.env)
        if query is not None:
            raise Exception("数据已存在, 请勿重复添加")
        data = PityRedis(**form.dict(), user=user_info['id'])
        result = await PityRedisConfigDao.insert_record(data)
        return PityResponse.success(data=PityResponse.model_to_dict(result))
    except Exception as err:
        return PityResponse.failed(err)


@router.post("/redis/update")
async def update_redis_config(form: RedisConfigForm,
                              user_info=Depends(Permission(Config.ADMIN))):
    try:
        result = await PityRedisConfigDao.update_record_by_id(user_info['id'], form)
        return PityResponse.success(data=PityResponse.model_to_dict(result))
    except Exception as err:
        return PityResponse.failed(err)


@router.get("/redis/delete")
async def delete_redis_config(id: int,
                              user_info=Depends(Permission(Config.ADMIN))):
    try:
        await PityRedisConfigDao.delete_record_by_id(user_info['id'], id)
        return PityResponse.success()
    except Exception as err:
        return PityResponse.failed(err)
